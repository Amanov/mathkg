from datetime import datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Account


#registration of user working code


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Бардык жарактуу электрондук почта дареги')
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type':'date','max':datetime.now().date()}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "GET"
        self.helper.add_input(Submit('submit', 'Submit'))
        # Help text
        self.helper['username'].help_text = 'Колдонуучунун атын тандаңыз'
        self.fields['password1'].help_text = 'Сырсөзүңүз башка жеке маалыматыңызга өтө окшош болбошу керек.Сырсөзүңүз кеминде 8 белгиден турушу керек.Сырсөзүңүз көп колдонулган сырсөз болушу мүмкүн эмес.Сырсөзүңүз толугу менен сандык болбошу керек.'
        self.fields['password2'].help_text = "Текшерүү үчүн мурункудай эле паролду тастыктаңыз."
        self.fields['date_of_birth'].help_text = "Туулга кунунуз"
        # Label name customization
        self.fields['email'].label = "Электрондук почта"
        self.fields['username'].label = "Колдонуучунун аты"
        self.fields['password1'].label = "Сырсөз"
        self.fields['password2'].label = "Сырсөз Тастыктаңыз"
        self.fields['date_of_birth'].label = "Туулган жылыңыз"

    class Meta:
        model = Account
        fields = ("email", "username", "password1", "password2", "date_of_birth")
      
        help_texts = {
            'username': 'Колдонуучунун атын тандаңыз ',
        }

#Login of user
class AccountAuthenticationForm(forms.Form):
    # Plain Form, not ModelForm: a ModelForm bound to Account here would run
    # Account.email's unique=True validator on every login attempt, which
    # always fails with "Account with this Email already exists" for any
    # real user (the whole point of logging in is that the account already
    # exists) - login was completely broken for every user because of this.

    email = forms.EmailField(label="Электрондук почта",max_length=60, help_text='Катталган электрондук почта дарегиниз')

    password = forms.CharField(label='Сырсөз', widget=forms.PasswordInput,help_text='Катталууда жазган паролуңуз')

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password and not authenticate(email=email, password=password):
            raise forms.ValidationError('Кирүү жараксыз же админ сиздин аккаунтуңузду активдештирген эмес, админге кайрылыңыз ')
        return cleaned_data

#Account[user info] Update

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model=Account
        fields = ('email', 'username')

    #emailin checking
    def clean_email(self):
        email = self.cleaned_data['email']
        if Account.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Электерондук почта "%s" башка бирөө тарабынан колдонулуп жатат.' % email)
        return email

    #username checking
    def clean_username(self):
        username = self.cleaned_data['username']
        if Account.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Бул колдонуучу "%s" башка бирөө тарабынан колдонулуп жатат.' % username)
        return username

