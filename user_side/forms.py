from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import validators
from .models import User
import re

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'mobile', 'password']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Mobile Number'

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        mobile = ''.join(filter(str.isdigit, mobile))

        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must have exactly 10 digits.")

        if ' ' in mobile:
            raise forms.ValidationError("Mobile number cannot contain spaces.")

        return mobile

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if ' ' in password:
            raise forms.ValidationError("Password cannot contain spaces.")

        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return password

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        # if not first_name[0].isupper():
        #         raise forms.ValidationError("The first letter of the first name should be capitalized.")

        if ' ' in first_name:
            raise forms.ValidationError("First name cannot contain spaces.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if ' ' in last_name:
            raise forms.ValidationError("Last name cannot contain spaces.")

        return last_name

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile']

class ProfileEditForm(UserProfileForm):
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if ' ' in first_name:
            raise forms.ValidationError("First name cannot contain spaces.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if ' ' in last_name:
            raise forms.ValidationError("Last name cannot contain spaces.")

        return last_name

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        
        mobile = re.sub(r'\D', '', mobile)

        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must have exactly 10 digits.")

        if not mobile.isdigit():
            raise forms.ValidationError("Mobile number should contain only digits.")

        return mobile
