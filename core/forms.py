from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as DefaultPasswordChangeForm
from django.contrib.auth import get_user_model
from .models import Appointment, TATTOO_LOCATION, APPOINTMENT_STATUS, TATTOO_CATEGORY, TATTOO_SIZE, Artist, PREFERRED_CONTACT_WAY


class RegisterForm(UserCreationForm):
    # fields we want to include and customize in our form
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                               'class': 'form-control',
                                                               }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email',
                                                           'class': 'form-control',
                                                           }))
    phone_number = forms.CharField(min_length=10,
                                   max_length=10,
                                   required=True,
                                   widget=forms.TextInput(attrs={'placeholder': 'Phone number',
                                                                 'class': 'form-control',
                                                                }))
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).count() > 0:
            raise forms.ValidationError("We already have a user with this email")
        return data

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalnum():
            raise forms.ValidationError('Please use letters only for your first name')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalnum():
            raise forms.ValidationError('Please use letters only for your last name')
        return last_name

    def clean_phone_number(self):
        special_characters = "'!@#$%^&*()-+?_=,<>/"
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isnumeric:
            raise forms.ValidationError('Please use numbers only for phone number, no need to include +44')
        if any(c in special_characters for c in phone_number):
            raise forms.ValidationError('Please use numbers only for phone number, no need to include +44')
        if '"' in phone_number:
            raise forms.ValidationError('Please use numbers only for phone number, no need to include +44')
        return phone_number

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']