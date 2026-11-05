from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST


@login_required
@require_POST
def tour_seen_view(request):
    tour = request.POST.get('tour')
    if tour == 'welcome':
        request.user.tour_seen = True
        request.user.save(update_fields=['tour_seen'])
    elif tour == 'test':
        request.user.test_tour_seen = True
        request.user.save(update_fields=['test_tour_seen'])
    else:
        return HttpResponseBadRequest('Белгисиз көрсөтмө.')
    return HttpResponse(status=204)
