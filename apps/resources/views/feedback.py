"""Page-face reactions and the written feedback form."""
from urllib.parse import urlparse

from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from django_ratelimit.decorators import ratelimit

from apps.resources.models import PageReaction, WrittenFeedback
from apps.resources.reactions import (
    already_voted,
    clean_public_path,
    record_reaction,
    remember_vote,
    visitor_key,
)
from apps.resources.utils.request_helpers import get_client_ip

RATE_MESSAGE = 'Билдирүү өтө көп жөнөтүлдү. Бир аздан кийин кайталаңыз.'


def _limit_key(group, request):
    return get_client_ip(request) or 'unknown'


class WrittenFeedbackForm(forms.Form):
    kind = forms.ChoiceField(
        label='Түрү',
        choices=WrittenFeedback.KIND_CHOICES,
        widget=forms.RadioSelect,
        error_messages={
            'required': 'Түрүн тандаңыз.',
            'invalid_choice': 'Түрүн тандаңыз.',
        },
    )
    message = forms.CharField(
        label='Билдирүү',
        max_length=4000,
        widget=forms.Textarea(attrs={
            'rows': 6,
            'placeholder': 'Оюңузду ушул жерге жазыңыз',
        }),
        error_messages={
            'required': 'Билдирүүнү жазыңыз.',
            'max_length': 'Билдирүү өтө узун.',
        },
    )
    name = forms.CharField(
        label='Аты-жөнү',
        max_length=120,
        required=False,
    )
    email = forms.EmailField(
        label='Электрондук почта',
        required=False,
        error_messages={'invalid': 'Электрондук почта туура эмес.'},
    )
    about_page = forms.CharField(
        label='Кайсы барак жөнүндө',
        max_length=255,
        required=False,
    )
    # Filled only by bots. A person never sees it.
    mk_hp = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'tabindex': '-1',
        'autocomplete': 'off',
        'aria-hidden': 'true',
    }))

    def clean_message(self):
        text = (self.cleaned_data.get('message') or '').strip()
        if len(text) < 2:
            raise ValidationError('Билдирүүнү жазыңыз.')
        return text

    def clean_name(self):
        return (self.cleaned_data.get('name') or '').strip()

    def clean_about_page(self):
        return (self.cleaned_data.get('about_page') or '').strip()

    def clean_email(self):
        return (self.cleaned_data.get('email') or '').strip()


def _referer_path(request):
    raw = request.META.get('HTTP_REFERER', '')
    if not raw:
        return ''
    parts = urlparse(raw)
    if parts.netloc and parts.netloc != request.get_host():
        return ''
    path = parts.path or ''
    if not path.startswith('/') or path.startswith('//') or '..' in path:
        return ''
    if path in ('/pikir/', '/pikirler/'):
        return ''
    return path[:255]


def _wants_json(request):
    return request.headers.get('X-Requested-With') == 'fetch'


@require_POST
@ratelimit(key=_limit_key, rate='30/m', method='POST', block=False)
def page_reaction_view(request):
    path = clean_public_path(request.POST.get('path'))
    face = (request.POST.get('face') or '').strip()
    visitor = visitor_key(request)
    counted = False

    if path and face in dict(PageReaction.FACE_CHOICES) and not getattr(request, 'limited', False):
        if already_voted(request, path):
            counted = False
        else:
            counted = record_reaction(path, face, visitor)

    if _wants_json(request):
        status = 200 if path and face in dict(PageReaction.FACE_CHOICES) else 400
        if getattr(request, 'limited', False):
            status = 429
        response = JsonResponse({'ok': status == 200, 'saved': counted}, status=status)
    elif path:
        response = redirect(path)
    else:
        response = redirect('home')

    if path and face in dict(PageReaction.FACE_CHOICES) and not getattr(request, 'limited', False):
        remember_vote(response, request, visitor, path)
    return response


@require_http_methods(['GET', 'POST'])
@ratelimit(key=_limit_key, rate='5/h', method='POST', block=False)
def feedback_view(request):
    initial = {}
    if request.method == 'GET':
        initial['about_page'] = _referer_path(request)
    form = WrittenFeedbackForm(request.POST or None, initial=initial)
    sent = False

    if request.method == 'POST':
        if getattr(request, 'limited', False):
            form.add_error(None, RATE_MESSAGE)
        elif form.is_valid():
            # A filled honeypot looks like success and is not stored.
            if not (form.cleaned_data.get('mk_hp') or '').strip():
                WrittenFeedback.objects.create(
                    kind=form.cleaned_data['kind'],
                    message=form.cleaned_data['message'],
                    name=form.cleaned_data['name'],
                    email=form.cleaned_data['email'],
                    about_page=form.cleaned_data['about_page'],
                )
            sent = True

    return render(request, 'resources/feedback.html', {
        'form': form,
        'sent': sent,
    })


def teacher_comments_view(request):
    notes = WrittenFeedback.objects.filter(show_on_site=True)
    return render(request, 'resources/teacher_comments.html', {
        'notes': notes,
    })
