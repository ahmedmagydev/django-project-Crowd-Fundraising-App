from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import UserProfile
# from phone_field import PhoneField
from django.core.validators import RegexValidator


class UserRegistrationForm(UserCreationForm):
    # email = forms.CharField(max_length=255,required=True,widget=forms.EmailInput())
    # photo = forms.ImageField()
    # phone = forms.CharField(error_messages={'incomplete': 'Enter a country calling code.'},validators=[RegexValidator(r'^[0-9]+$', 'Enter a valid country calling code.'),])
    # firstname = forms.CharField(max_length=100, required=False)
    # lastname = forms.CharField(max_length=100, required=False)
    # class Meta:
    #     model=User
    #     fields = ['firstname','lastname','username','email','password1','password2']
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'first_name', 'last_name',
                  'phone', 'photo', 'password1', 'password2')

    # def save(self, commit=True):
    #     user = super(UserRegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = UserProfile
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
