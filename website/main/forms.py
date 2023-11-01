from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=50)
    username = forms.CharField(required=True, max_length=50)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True,
        max_length=100,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        required=True,
        max_length=100,
    )
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
