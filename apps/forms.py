from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

from apps.models import User, Emails


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-type Password'}))

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Confirm password is not correct')
        return make_password(password)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'confirm_password')


class EmailForm(forms.ModelForm):
    def clean_email(self):
        email = self.data.get('email')
        if Emails.objects.filter(email=email):
            raise ValidationError('Email already exists !')
        return email

    class Meta:
        model = Emails
        fields = ('email',)
