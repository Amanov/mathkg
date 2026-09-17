from .models import PaymentQRCode


def active_qr_code(request):
    return {
        'active_payment_qr': PaymentQRCode.objects.filter(is_active=True).first(),
    }
