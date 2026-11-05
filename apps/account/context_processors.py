from .models import PaymentQRCode


def active_qr_code(request):
    return {
        'active_payment_qr': PaymentQRCode.objects.filter(is_active=True).first(),
    }


def tour_flags(request):
    user = getattr(request, 'user', None)
    if not user or not user.is_authenticated:
        return {'show_welcome_tour': False, 'show_test_tour': False}
    return {
        'show_welcome_tour': not user.tour_seen,
        'show_test_tour': not user.test_tour_seen,
    }
