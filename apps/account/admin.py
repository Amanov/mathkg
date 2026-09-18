from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, PaymentQRCode, SubscriptionRequest
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account,AccountAdmin)


@admin.register(PaymentQRCode)
class PaymentQRCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'is_active', 'updated_at')
    list_filter = ('is_active',)

    @admin.display(description='Булагы')
    def source(self, obj):
        return obj.link or "Жүктөлгөн сүрөт"

    def save_model(self, request, obj, form, change):
        # Only one QR code should ever be "the" one shown on the site -
        # activating this one deactivates any other, instead of relying
        # on whoever uploads it to remember to uncheck the old one.
        if obj.is_active:
            PaymentQRCode.objects.exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)


@admin.register(SubscriptionRequest)
class SubscriptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'created_at')
    list_filter = ('plan', 'status')
    search_fields = ('user__email', 'user__username')
    actions = ['confirm_and_activate']

    @admin.action(description='Тандалган: төлөмдү ырастоо жана жазылууну активдештирүү')
    def confirm_and_activate(self, request, queryset):
        confirmed = 0
        for subscription_request in queryset.filter(status=SubscriptionRequest.STATUS_PENDING):
            subscription_request.activate()
            confirmed += 1
        self.message_user(request, f"{confirmed} жазылуу активдештирилди.")

    def save_model(self, request, obj, form, change):
        # This model has no fields/readonly_fields restriction, so nothing
        # stops a site owner from just opening a request and flipping the
        # Status dropdown on its own edit page instead of using the bulk
        # action above. Saved the ordinary way, that silently persists
        # "confirmed" without ever extending the account's
        # subscription_end (only activate() does that) - the request
        # *looks* confirmed but the user gets no actual access. Route
        # that path through activate() too, so confirming a payment has
        # the same effect no matter which page it's done from.
        becoming_confirmed = (
            change
            and form.initial.get('status') == SubscriptionRequest.STATUS_PENDING
            and obj.status == SubscriptionRequest.STATUS_CONFIRMED
        )
        if becoming_confirmed:
            obj.status = SubscriptionRequest.STATUS_PENDING
            super().save_model(request, obj, form, change)
            obj.activate()
        else:
            super().save_model(request, obj, form, change)

