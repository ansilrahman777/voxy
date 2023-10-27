from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import validators
from .models import User,ReviewRating,Wallet
import re
import phonenumbers
from phonenumbers import is_valid_number

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control', 
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control', 
    }))
    referral_code = forms.CharField(max_length=10, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Referral Code (optional)',
        'class': 'form-control', 

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
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email.lower().endswith('@gmail.com'):
            raise forms.ValidationError("Please enter a valid Gmail address.")

        return email

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        mobile = ''.join(filter(str.isdigit, mobile))

        if len(mobile) != 10:
            raise forms.ValidationError("Mobile number must have exactly 10 digits.")

        if ' ' in mobile:
            raise forms.ValidationError("Mobile number cannot contain spaces.")

        if not re.match(r'^[789]\d{9}$', mobile):
            raise forms.ValidationError("Please enter a valid mobile number.")

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

        

        invalid_characters = [' ', '*', '#', '@', '$', '(', '+', '-', '!', '^', '&']
        if any(char in first_name for char in invalid_characters):
            raise forms.ValidationError("First name cannot contain invalid characters.")

        if len(first_name) < 4:
            raise forms.ValidationError("First name is very short.")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        invalid_characters = [' ', '*', '#', '@', '$', '(', '+', '-', '!', '^', '&']
        if any(char in last_name for char in invalid_characters):
            raise forms.ValidationError("First name cannot contain invalid characters.")

        return last_name

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password doesn't match")

    def clean_referral_code(self):
        referral_code = self.cleaned_data.get('referral_code')

        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist: 
                raise forms.ValidationError("Invalid referral code")

        return referral_code

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile']

class ProfileEditForm(UserProfileForm):
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        invalid_characters = [' ', '*', '#','@','$','(','+','-','!','^','&']

        if any(char in first_name for char in invalid_characters):
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

class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = ReviewRating
        fields = ['subject','review','rating']
