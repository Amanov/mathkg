from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from datetime import datetime

#registration of user working code
class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=60, help_text='Бардык жарактуу электрондук почта дареги')
    date_of_birth =forms.DateField(widget=forms.DateInput(attrs={'type':'date','max':datetime.now().date()}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method="GET"
        self.helper.add_input(Submit('submit','Submit'))
        # Help text
        self.helper['username'].help_text='Колдонуучунун атын тандаңыз'
        self.fields['password1'].help_text='Сырсөзүңүз башка жеке маалыматыңызга өтө окшош болбошу керек.Сырсөзүңүз кеминде 8 белгиден турушу керек.Сырсөзүңүз көп колдонулган сырсөз болушу мүмкүн эмес.Сырсөзүңүз толугу менен сандык болбошу керек.'
        self.fields['password2'].help_text="Текшерүү үчүн мурункудай эле паролду тастыктаңыз."
        self.fields['date_of_birth'].help_text ="Туулга кунунуз"
        # Label name customization
        self.fields['email'].label = "Электрондук почта"
        self.fields['username'].label = "Колдонуучунун аты"
        self.fields['password1'].label = "Сырсөз"
        self.fields['password2'].label = "Сырсөз Тастыктаңыз"
        self.fields['date_of_birth'].label = "Туулган жылыңыз"


        



    class Meta:
        model = Account
        fields = ("email","username","password1","password2","date_of_birth")
      
        help_texts = {
           
            'username': 'Колдонуучунун атын тандаңыз ',
            
        }
        

# Here we have customized crispy
# class RegistrationForm(forms.Form):
#     field1 = forms.CharField(label='Field 1')
#     field2 = forms.EmailField(label='Field 2')

#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Field('field1', css_class='custom-class'),
#             Field('field2', css_class='custom-class'),
#             Submit('submit', 'Submit', css_class='btn btn-primary')
#         )

# #School registraion form we will work later 

# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(max_length=60, help_text='Бардык жарактуу электрондук почта дареги')
    

#     class Meta:
#         model = Account
#         fields = ("email","username","password1","password2")


#Login of user
class AccountAuthenticationForm(forms.ModelForm):
    
    email = forms.EmailField(label="Электрондук почта",max_length=60, help_text='Жарактуу электрондук почта дареги')

    password = forms.CharField(label='Сырсөз', widget=forms.PasswordInput,help_text='Сиздин паролуңуз')

    

    class Meta:
        model =Account
        fields =('email', 'password')

    def clean(self):
        if self.is_valid():
            email =self.cleaned_data['email']
            password =self.cleaned_data['password']
            if not authenticate(email=email,password = password):
                raise forms.ValidationError('Кирүү жараксыз же админ сиздин аккаунтуңуз активдештирилген эмес, админге кайрылыңыз ')
            
#Account[user info] Update 

class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model=Account
        fields = ('email', 'username')

    #emailin checking 
    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account =Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)
        
    #password checking
    def clean_username(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account =Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % username)
        
