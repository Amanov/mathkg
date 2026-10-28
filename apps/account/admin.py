from datetime import timedelta

from django.contrib import admin, messages
from django.contrib.admin.actions import delete_selected
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.contrib.auth.admin import UserAdmin
from django.db import IntegrityError, router, transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _

from .models import Account, PaymentQRCode, SubscriptionRequest

# Shown when COMMIT rejects the delete (a foreign key Django does not
# know about). The account row is unchanged. Kept in Kyrgyz to match
# the other staff-facing messages on this admin.
ACCOUNT_DELETE_BLOCKED = (
    'Аккаунт өчпөй калды: аны башка жазуу шилтеп турат. Аккаунт ордунда калды.'
)


def delete_selected_honestly(modeladmin, request, queryset):
    # The stock action adds its success message only after
    # queryset.delete() returns. That delete commits its own
    # transaction, so a failed COMMIT raises before the message.
    # Catch it here and say the rows stayed, instead of a bare 500.
    try:
        return delete_selected(modeladmin, request, queryset)
    except IntegrityError:
        modeladmin.message_user(request, ACCOUNT_DELETE_BLOCKED, messages.ERROR)
        return None


# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')

    filter_horizontal =()
    list_filter = ()
    fieldsets = ()
    actions = ['end_subscription_for_violation']

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            _func, name, description = actions['delete_selected']
            actions['delete_selected'] = (delete_selected_honestly, name, description)
        return actions

    def delete_view(self, request, object_id, extra_context=None):
        # ModelAdmin.delete_view commits the surrounding atomic block
        # after response_delete() has already queued the success
        # message. Postgres checks deferred foreign keys at that
        # COMMIT. On failure the account is restored, but
        # MessageMiddleware still saves the success message onto the
        # 500 response. response_delete() below waits for on_commit;
        # this except reports the rollback in the admin instead.
        try:
            return super().delete_view(request, object_id, extra_context)
        except IntegrityError:
            self.message_user(request, ACCOUNT_DELETE_BLOCKED, messages.ERROR)
            post_url = reverse(
                'admin:%s_%s_changelist' % (self.opts.app_label, self.opts.model_name),
                current_app=self.admin_site.name,
            )
            return HttpResponseRedirect(post_url)

    def response_delete(self, request, obj_display, obj_id):
        # Popup closes without the green banner. The normal path must
        # not call message_user until the delete_view transaction has
        # committed, or a deferred constraint failure leaves a success
        # banner on an account that is still there.
        if IS_POPUP_VAR in request.POST:
            return super().response_delete(request, obj_display, obj_id)

        def announce_deletion():
            self.message_user(
                request,
                _('The %(name)s “%(obj)s” was deleted successfully.')
                % {
                    'name': self.opts.verbose_name,
                    'obj': obj_display,
                },
                messages.SUCCESS,
            )

        transaction.on_commit(announce_deletion, using=router.db_for_write(self.model))

        if self.has_change_permission(request, None):
            post_url = reverse(
                'admin:%s_%s_changelist' % (self.opts.app_label, self.opts.model_name),
                current_app=self.admin_site.name,
            )
            preserved_filters = self.get_preserved_filters(request)
            post_url = add_preserved_filters(
                {'preserved_filters': preserved_filters, 'opts': self.opts},
                post_url,
            )
        else:
            post_url = reverse('admin:index', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)

    @admin.action(description='Эрежелерди бузгандыгы үчүн жазылууну токтотуу жана бөгөттөө')
    def end_subscription_for_violation(self, request, queryset):
        # Immediate and permanent until someone manually reverses it -
        # this is meant for a real ToS violation, not a routine expiry.
        # Setting subscription_end into the past (rather than clearing
        # it to null) matters: null falls back to the signup trial on
        # Account.subscription_end_date (trial_days from the local
        # signup date), which would leave access in place instead of
        # cutting it off. is_active=False additionally blocks login
        # entirely, not just paid downloads.
        yesterday = timezone.localdate() - timedelta(days=1)
        count = 0
        for account in queryset:
            account.subscription_end = yesterday
            account.is_active = False
            account.save(update_fields=['subscription_end', 'is_active'])
            self.log_change(
                request, account,
                "Эрежелерди/макулдашууну бузгандыгы үчүн жазылуу токтотулду жана аккаунт бөгөттөлдү.",
            )
            count += 1
        self.message_user(
            request, f"{count} колдонуучунун жазылуусу токтотулду жана аккаунту бөгөттөлдү.",
            level=messages.WARNING,
        )

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


class StatusDefaultsToPendingFilter(admin.SimpleListFilter):
    # A plain ('status',) entry in list_filter has no concept of a
    # default - landing on the list with no filter chosen shows every
    # request ever confirmed, burying new pending ones underneath. This
    # makes "no filter chosen yet" behave as if "Төлөм күтүлүүдө" were
    # selected, while still offering a real "Бардыгы" option (its own
    # explicit value, not just the absence of a param) to see everything
    # on demand - nothing is hidden permanently or deleted.
    title = 'абалы'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return list(SubscriptionRequest.STATUS_CHOICES) + [('all', 'Бардыгы')]

    def queryset(self, request, queryset):
        value = self.value()
        if value is None:
            return queryset.filter(status=SubscriptionRequest.STATUS_PENDING)
        if value == 'all':
            return queryset
        return queryset.filter(status=value)

    def choices(self, changelist):
        value = self.value()
        for lookup, title in self.lookup_choices:
            yield {
                'selected': value == lookup or (value is None and lookup == SubscriptionRequest.STATUS_PENDING),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}),
                'display': title,
            }


@admin.register(SubscriptionRequest)
class SubscriptionRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'activation_status', 'created_at')
    list_filter = ('plan', StatusDefaultsToPendingFilter)
    search_fields = ('user__email', 'user__username')
    actions = ['confirm_and_activate']

    @admin.display(description='Активдештирилдиби')
    def activation_status(self, obj):
        # Surfaces the exact failure mode that motivated activated_at:
        # a request whose status shows "Төлөндү" but was never actually
        # run through activate(), so the account's subscription_end was
        # never extended despite looking confirmed.
        if obj.status != SubscriptionRequest.STATUS_CONFIRMED:
            return "—"
        if obj.activated_at:
            return obj.activated_at.strftime('%Y-%m-%d %H:%M')
        return "ЖОК - колдонуучу али активдештирилген эмес"

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
        # change is False when the row is being created. Confirming on
        # the add form used to save status=confirmed and skip activate(),
        # the same "looks paid, access never granted" hole as editing
        # the status dropdown. A brand-new pending request is not this
        # path and must not grant access.
        becoming_confirmed = obj.status == SubscriptionRequest.STATUS_CONFIRMED and (
            not change
            or form.initial.get('status') == SubscriptionRequest.STATUS_PENDING
        )
        if becoming_confirmed:
            obj.status = SubscriptionRequest.STATUS_PENDING
            super().save_model(request, obj, form, change)
            obj.activate()
        else:
            super().save_model(request, obj, form, change)

