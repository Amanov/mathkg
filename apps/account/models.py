import calendar
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from config.storage_backends import persistent_media_storage

#creating custom users
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")
        
        user =self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    #creating superuser/admin
    def create_superuser(self, email, username, password):
        user =self.create_user(
            email=self.normalize_email(email),
            password =password,
            username=username,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True
        user.save(using=self._db)
        return user
        


class Account(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)  
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True) #date joined
    # No auto_now: Django's own login signal (update_last_login) sets this
    # on actual login. auto_now was overwriting it to "now" on every save
    # of the account (admin edits, subscription updates, etc.).
    last_login              = models.DateTimeField(verbose_name='last_login', null=True, blank=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=False) #activation of user
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    # first_name              =models.CharField(max_length=30)
    #
    # ✅ Subscription end date field
    subscription_end = models.DateField(null=True, blank=True)

    # A teacher belongs to at most one school. School itself is defined
    # below (staff assign schools/admins via Django admin for now - no
    # self-serve "create a school" flow yet), hence the string reference.
    school = models.ForeignKey(
        'School', null=True, blank=True, on_delete=models.SET_NULL, related_name='teachers',
    )
    is_school_admin = models.BooleanField(
        default=False,
        help_text="Мектептин башкаруучусу - өз мектебиндеги мугалимдерди көзөмөлдөй жана башкара алат.",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]  #'first_name' we can add a list

    objects = MyAccountManager()


    def __str__(self):
        return self.email  
    
    def has_perm(self, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def subscription_end_date(self):
        # Hybrid: an explicit subscription_end wins; otherwise every
        # account gets a 1-year trial from signup. Shared here so the
        # account page and any access-gating check agree on the same date.
        return self.subscription_end or (self.date_joined.date() + timedelta(days=365))

    @property
    def has_active_subscription(self):
        return self.subscription_end_date >= timezone.now().date()


class School(models.Model):
    name = models.CharField(max_length=255, verbose_name="Мектептин аталышы")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Мектеп"
        verbose_name_plural = "Мектептер"

    def __str__(self):
        return self.name


def add_months(base_date, months):
    """Adds exact calendar months to a date (not a fixed day-count
    approximation), clamping the day when the target month is shorter -
    e.g. 31 Jan + 1 month -> 28/29 Feb, not an overflow into March."""
    month_index = base_date.month - 1 + months
    year = base_date.year + month_index // 12
    month = month_index % 12 + 1
    day = min(base_date.day, calendar.monthrange(year, month)[1])
    return base_date.replace(year=year, month=month, day=day)


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)
    else:
        pass

## I want to count how many times file is downloaded

class DownloadFile(models.Model):
    name            = models.CharField(max_length=255)
    file            = models.FileField(upload_to='downloads/')
    slug            = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    
    # ─── add / keep these ───
    download_count  = models.PositiveIntegerField(default=0, editable=False)
    last_downloaded = models.DateTimeField(null=True, blank=True, editable=False)

    def increment_download(self):
        self.download_count += 1
        self.last_downloaded = timezone.now()
        self.save(update_fields=['download_count', 'last_downloaded'])

    def __str__(self):
        return f"{self.name} ({self.download_count})"


class PaymentQRCode(models.Model):
    # A single admin-managed image rather than a hardcoded static file,
    # since the underlying payment account/QR needs to be swapped every
    # few months without a code deploy. is_active lets an old one be kept
    # around (for records) while only ever showing one at a time.
    #
    # Two ways to provide it: upload a QR image directly, or paste a
    # payment link (e.g. from finik.kg) and have the QR generated from
    # it here - Finik hands out a payment URL, not a hosted image, so
    # there's nothing to just point an <img> tag at. Either way the
    # result lands in `image`, so every template/view that displays this
    # (the subscribe modal) reads one field regardless of which path
    # produced it.
    image = models.ImageField(upload_to='payment_qr/', blank=True, storage=persistent_media_storage)
    link = models.URLField(
        blank=True,
        verbose_name="Төлөм шилтемеси (Finik.kg ж.б.)",
        help_text="Эгер сүрөт жүктөбөсөңүз, ушул жерге төлөм шилтемесин коюңуз - QR код автоматтык түрдө түзүлөт.",
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Төлөм QR коду"
        verbose_name_plural = "Төлөм QR коддору"

    def __str__(self):
        return f"QR ({'активдүү' if self.is_active else 'эски'}, {self.updated_at:%Y-%m-%d})"

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.image and not self.link:
            raise ValidationError("Сүрөттү жүктөңүз же төлөм шилтемесин киргизиңиз.")
        if self.image and self.link:
            raise ValidationError("Экөөнүн бирин гана тандаңыз: жүктөлгөн сүрөт же шилтеме.")

    def save(self, *args, **kwargs):
        if self.link:
            import io
            import qrcode
            from django.core.files.base import ContentFile

            buffer = io.BytesIO()
            qrcode.make(self.link).save(buffer, format='PNG')
            self.image.save('qr_from_link.png', ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)


class SubscriptionRequest(models.Model):
    PLAN_THREE_MONTHS = '3m'
    PLAN_SIX_MONTHS = '6m'
    PLAN_ONE_YEAR = '1y'
    PLAN_CHOICES = [
        (PLAN_THREE_MONTHS, '3 ай - 1499 сом'),
        (PLAN_SIX_MONTHS, '6 ай - 2999 сом'),
        (PLAN_ONE_YEAR, '1 жыл - 4999 сом'),
    ]
    # Kept next to the choices they describe, instead of a separate
    # settings/constants file, since a plan here is meaningless without
    # both a duration and a price. Durations are exact calendar months
    # (via add_months), not a fixed day-count approximation - "6 months"
    # from different starting dates isn't always the same number of days.
    PLAN_MONTHS = {PLAN_THREE_MONTHS: 3, PLAN_SIX_MONTHS: 6, PLAN_ONE_YEAR: 12}
    PLAN_PRICE_SOM = {PLAN_THREE_MONTHS: 1499, PLAN_SIX_MONTHS: 2999, PLAN_ONE_YEAR: 4999}

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Төлөм күтүлүүдө'),
        (STATUS_CONFIRMED, 'Төлөндү'),
    ]

    user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='subscription_requests',
    )
    plan = models.CharField(max_length=2, choices=PLAN_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    # Set only by activate() itself - lets admin tell a request that was
    # genuinely confirmed apart from one whose status field was set some
    # other way (see SubscriptionRequestAdmin.save_model) without this
    # ever actually running, which is exactly the bug that left a paying
    # user's subscription_end untouched despite status showing "Төлөндү".
    activated_at = models.DateTimeField(null=True, blank=True, editable=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Жазылуу суранычы"
        verbose_name_plural = "Жазылуу суранычтары"

    def __str__(self):
        return f"{self.user.email} - {self.get_plan_display()} ({self.get_status_display()})"

    def activate(self):
        # Idempotent on purpose: this runs from more than one admin path
        # (the bulk action, and a plain status-field edit on the object -
        # see SubscriptionRequestAdmin.save_model), so it must be safe to
        # call on an already-confirmed request without extending the
        # account a second time for one payment.
        if self.status == self.STATUS_CONFIRMED:
            return

        today = timezone.now().date()
        # Stacks on top of a real remaining *paid* period - so renewing
        # a still-active plan early adds to the remaining time instead
        # of resetting it - but never on top of the free signup trial.
        # self.user.subscription_end_date falls back to a synthesized
        # trial date (date_joined + 1 year) when subscription_end is
        # still null; stacking a new plan onto *that* is what let a
        # freshly-signed-up account paying for 6 months end up with
        # ~1.5 years of access instead of 6 months. Reading the raw
        # field instead of that hybrid property is what excludes it.
        current_paid_end = self.user.subscription_end
        base_date = max(today, current_paid_end) if current_paid_end else today
        self.user.subscription_end = add_months(base_date, self.PLAN_MONTHS[self.plan])
        # A verified payment is at least as strong proof of a real user as
        # clicking the signup activation email - so confirming one also
        # activates the account, rather than leaving login blocked on an
        # unrelated step a paying user may never have completed.
        self.user.is_active = True
        self.user.save(update_fields=['subscription_end', 'is_active'])
        self.status = self.STATUS_CONFIRMED
        self.activated_at = timezone.now()
        self.save(update_fields=['status', 'activated_at'])



