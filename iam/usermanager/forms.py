from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User
from django.contrib.auth import (
    authenticate
    )

# User = get_user_model()

# User login form
class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = None
            # Try to authenticate with username
            user = authenticate(username=username, password=password)

            # If authentication with username fails, try with email
            if not user:
                user = User.objects.filter(email=username).first()
                if user:
                    user = authenticate(username=user.username, password=password)

            # If authentication with email fails, try with primary phone
            if not user:
                user = User.objects.filter(primary_phone=username).first()
                if user:
                    user = authenticate(username=user.username, password=password)

            # If user is still not found or password is incorrect, raise validation error
            if not user or not user.check_password(password):
                raise forms.ValidationError('Invalid username/email/phone or password')

            # If user is not active, raise validation error
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

            cleaned_data['user'] = user

        return cleaned_data

class UserRegisterForm(forms.ModelForm):
    # username = forms.CharField(label='Username')
    email = forms.EmailField(label='Email address')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]

    def clean(self, *args, **kwargs):
        # username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email has already been registered")
        return super(UserRegisterForm, self).clean(*args, **kwargs)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)