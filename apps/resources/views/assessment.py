from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.resources.assessment import (
    NotEnoughQuestions,
    QuotaExceeded,
    create_generated_test,
    initial_from_query,
    monthly_usage,
    published_topic_stats,
    render_test_pdf,
    TestMakerForm,
)
from apps.resources.models import GeneratedTest


@login_required
def test_maker_view(request):
    topic_stats = published_topic_stats()
    usage = monthly_usage(request.user)
    if request.method == 'POST':
        form = TestMakerForm(request.POST, topic_stats=topic_stats)
        if form.is_valid():
            try:
                generated = create_generated_test(request.user, form.cleaned_data)
            except NotEnoughQuestions as exc:
                form.add_error(None, str(exc))
            except QuotaExceeded as exc:
                form.add_error(None, str(exc))
            else:
                return redirect('test_maker_result', pk=generated.pk)
    else:
        form = TestMakerForm(
            initial=initial_from_query(request, topic_stats),
            topic_stats=topic_stats,
        )
    return render(request, 'resources/test_maker.html', {
        'form': form,
        'usage': usage,
        'has_questions': bool(topic_stats),
    })


@login_required
def test_maker_result_view(request, pk):
    generated = get_object_or_404(GeneratedTest, pk=pk, user=request.user)
    return render(request, 'resources/test_maker_result.html', {
        'generated': generated,
        'paper': generated.payload,
        'usage': monthly_usage(request.user),
    })


@login_required
def test_maker_pdf_view(request, pk):
    generated = get_object_or_404(GeneratedTest, pk=pk, user=request.user)
    pdf = render_test_pdf(generated.payload)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="mathkg-{generated.grade}-klass-test.pdf"'
    )
    return response
