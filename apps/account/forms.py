from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import BaseUserCreationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Account


_REQUIRED = 'Бул талаа толтурулушу керек.'


class _KyrgyzSimilarityValidator(password_validation.UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        try:
            super().validate(password, user)
        except ValidationError:
            raise ValidationError(
                'Сырсөз башка жеке маалыматыңызга өтө окшош.',
                code='password_too_similar',
            )


class _KyrgyzMinimumLengthValidator(password_validation.MinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                'Сырсөз кеминде %(min_length)d белгиден турушу керек.',
                code='password_too_short',
                params={'min_length': self.min_length},
            )


class _KyrgyzCommonPasswordValidator(password_validation.CommonPasswordValidator):
    def validate(self, password, user=None):
        if password.lower().strip() in self.passwords:
            raise ValidationError(
                'Бул сырсөз өтө көп колдонулат.',
                code='password_too_common',
            )


class _KyrgyzNumericPasswordValidator(password_validation.NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                'Сырсөз сандан гана турбашы керек.',
                code='password_entirely_numeric',
            )


KYRGYZ_PASSWORD_VALIDATORS = [
    _KyrgyzSimilarityValidator(),
    _KyrgyzMinimumLengthValidator(),
    _KyrgyzCommonPasswordValidator(),
    _KyrgyzNumericPasswordValidator(),
]


class RegistrationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': 'Эки сырсөз дал келген жок.',
    }
    email = forms.EmailField(
        max_length=60,
        label='Электрондук почта',
        help_text='Жарактуу электрондук почта дарегиңиз',
        error_messages={
            'required': _REQUIRED,
            'invalid': 'Электрондук почтанын дареги туура эмес.',
        },
    )
    date_of_birth = forms.DateField(
        required=False,
        label='Туулган күнүңүз',
        help_text='Милдеттүү эмес.',
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={
            'invalid': 'Туулган күн туура эмес.',
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        # Must be POST: this form carries a password. It's currently
        # rendered via {{ form|crispy }} inside a manually-written
        # <form method="post">, which ignores this setting - but if that
        # template ever switches to {% crispy form %}, this value is what
        # decides the real HTTP method, and GET would leak passwords into
        # the URL, browser history and server logs.
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Катталуу'))
        self.fields['username'].label = 'Колдонуучунун аты'
        self.fields['username'].help_text = 'Колдонуучунун атын тандаңыз'
        self.fields['password1'].label = 'Сырсөз'
        self.fields['password1'].help_text = (
            'Сырсөзүңүз башка жеке маалыматыңызга өтө окшош болбошу керек. '
            'Кеминде 8 белгиден турушу керек. Көп колдонулган сырсөз болбошу керек. '
            'Сандан гана турбашы керек.'
        )
        self.fields['password2'].label = 'Сырсөздү тастыктаңыз'
        self.fields['password2'].help_text = 'Текшерүү үчүн ошол эле сырсөздү кайра жазыңыз.'
        # Evaluated per request, not at import, so the latest allowed day
        # is today rather than the day the process started.
        self.fields['date_of_birth'].widget.attrs['max'] = timezone.localdate().isoformat()

        for field in self.fields.values():
            field.error_messages.setdefault('required', _REQUIRED)
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' form-control').strip()

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2', 'date_of_birth')

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError('Бул электрондук почта мурунтан катталган.')
        return email

    def clean_username(self):
        # Case-insensitive, same as UserCreationForm.clean_username, but
        # the message stays Kyrgyz. The parent method's message is English.
        username = self.cleaned_data.get('username')
        if username and Account.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Бул колдонуучунун аты мурунтан катталган.')
        return username

    def clean_date_of_birth(self):
        value = self.cleaned_data.get('date_of_birth')
        if value and value > timezone.localdate():
            raise forms.ValidationError('Туулган күн келечекте болбошу керек.')
        return value

    def _get_validation_exclusions(self):
        # clean_email / clean_username already report a Kyrgyz unique
        # error. The model check would add a second, English one
        # ("Account with this email already exists").
        exclude = super()._get_validation_exclusions()
        exclude.update({'email', 'username'})
        return exclude

    def _post_clean(self):
        # Skip BaseUserCreationForm._post_clean: it runs Django's English
        # password validators. ModelForm._post_clean still builds the
        # instance. Kyrgyz validators below replace the English ones.
        super(BaseUserCreationForm, self)._post_clean()
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(
                    password,
                    self.instance,
                    password_validators=KYRGYZ_PASSWORD_VALIDATORS,
                )
            except ValidationError as error:
                self.add_error('password2', error)


class AccountAuthenticationForm(forms.Form):
    # Plain Form, not ModelForm: a ModelForm bound to Account here would run
    # Account.email's unique=True validator on every login attempt, which
    # always fails with "Account with this Email already exists" for any
    # real user (the whole point of logging in is that the account already
    # exists) - login was completely broken for every user because of this.

    email = forms.EmailField(
        label='Электрондук почта',
        max_length=60,
        help_text='Катталган электрондук почта дарегиңиз',
        error_messages={
            'required': _REQUIRED,
            'invalid': 'Электрондук почтанын дареги туура эмес.',
        },
    )

    password = forms.CharField(
        label='Сырсөз',
        widget=forms.PasswordInput,
        help_text='Катталууда жазган сырсөзүңүз',
        error_messages={'required': _REQUIRED},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    # No clean() override: this form only validates shape (a well-formed
    # email, a non-empty password). Actually authenticating - and telling
    # a wrong password apart from a correct one on a not-yet-activated
    # account - is login_view's job, since only it can show a different
    # message for each case. A clean() here that called authenticate()
    # itself used to make form.is_valid() False for both failure modes
    # before the view ever got a chance to tell them apart.


class AccountUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].error_messages['invalid'] = 'Электрондук почтанын дареги туура эмес.'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.error_messages['required'] = _REQUIRED

    class Meta:
        model = Account
        fields = ('email', 'username')

    def _get_validation_exclusions(self):
        # clean_email / clean_username already report a Kyrgyz unique
        # error. The model check would add an English one as well.
        exclude = super()._get_validation_exclusions()
        exclude.update({'email', 'username'})
        return exclude

    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Электрондук почта "%s" башка бирөө тарабынан колдонулуп жатат.' % email)
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if Account.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Бул колдонуучу "%s" башка бирөө тарабынан колдонулуп жатат.' % username)
        return username
