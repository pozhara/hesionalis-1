# Imports
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DefaultPasswordChangeForm
from django.contrib.auth import get_user_model

# Local imports
from .models import (Appointment,
                     TATTOO_LOCATION,
                     APPOINTMENT_STATUS,
                     TATTOO_CATEGORY,
                     TATTOO_SIZE,
                     Artist)


# Form class for registration
# https://dev.to/earthcomfy/creating-a-django-registration-login-app-part-i-1di5
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                    'placeholder': 'First Name',
                                    'class': 'form-control',
                                 }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'placeholder': 'Last Name',
                                    'class': 'form-control',
                                }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control',
                               }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={
                                'placeholder': 'Email',
                                'class': 'form-control',
                             }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Password',
                                    'class': 'form-control',
                                    'data-toggle': 'password',
                                    'id': 'password',
                                }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'placeholder': 'Confirm Password',
                                    'class': 'form-control',
                                    'data-toggle': 'password',
                                    'id': 'password',
                                }))

    # Email validation
    def clean_email(self):
        special_characters = "'!#$%^&*()-+?_=,<>/"
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("We already "
                                        "have a user with this email")
        if any(c in special_characters for c in data):
            raise forms.ValidationError("Only use letters, numbers, "
                                        "@ and . in your email.")
        if '"' in data:
            raise forms.ValidationError("Only use letters, numbers, "
                                        "@ and . in your email.")
        return data

    # First name validation
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalnum():
            raise forms.ValidationError('Please '
                                        'use letters only for your first name')
        return first_name

    # Last name validation
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalnum():
            raise forms.ValidationError('Please '
                                        'use letters only for your last name')
        return last_name

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'username', 'email', 'password1', 'password2']


# Form class for login
# https://dev.to/earthcomfy/creating-a-django-registration-login-app-part-i-1di5
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Username',
                                   'class': 'form-control',
                               }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Password',
                                   'class': 'form-control',
                                   'data-toggle': 'password',
                                   'id': 'password',
                                   'name': 'password',
                               }))
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']


# Form class for editing profile
class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=16,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                    'class': 'form-input',
                                    'autocomplete': 'off', }))
    last_name = forms.CharField(max_length=16,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-input',
                                    'autocomplete': 'off', }))

    # Validation for first name
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalnum():
            raise forms.ValidationError('Please '
                                        'use letters only for your first name')
        return first_name

    # Validation for last_name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalnum():
            raise forms.ValidationError('Please '
                                        'use letters only for your last name')
        return last_name

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


# Form class for password change
class PasswordChangeForm(DefaultPasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'autocomplete': 'off',
            'class': 'form-input'
        })
        self.fields['new_password1'].widget.attrs.update({
            'autocomplete': 'off',
            'class': 'form-input'
        })
        self.fields['new_password2'].widget.attrs.update({
            'autocomplete': 'off',
            'class': 'form-input'
        })


# Form class for appointment
class AppointmentForm(forms.ModelForm):
    tattoo_location = forms.ChoiceField(choices=TATTOO_LOCATION,
                                        required=True,
                                        widget=forms.Select(attrs={
                                           'class': 'form-input'}))
    tattoo_size = forms.ChoiceField(choices=TATTOO_SIZE,
                                    required=True,
                                    widget=forms.Select(attrs={
                                       'class': 'form-input'}))
    tattoo_category = forms.ChoiceField(choices=TATTOO_CATEGORY,
                                        required=True,
                                        widget=forms.Select(attrs={
                                            'class': 'form-input'}))
    artist = forms.ModelChoiceField(queryset=Artist.objects.all(),
                                    required=True,
                                    widget=forms.Select(attrs={
                                        'class': 'form-input'}))

    class Meta:
        model = Appointment
        fields = ['tattoo_location',
                  'tattoo_size', 'tattoo_category', 'artist']
