from django import forms
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm
from .models import CustomUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re


class CustomLoginForm(AuthenticationForm):
    # Rename 'username' field to accept Email/Phone/Username
    username = forms.CharField(
        label="Email, Phone, or Username",
        widget=forms.TextInput(attrs={
            "placeholder": "Phone, email, or username",
            }),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "name": "password",
            })
    )
    
    def clean_username(self):
        contact_info = self.cleaned_data.get('username').strip()

        # Check if input is email
        try:
            validate_email(contact_info)
            user = CustomUser.objects.filter(email =contact_info).first()
            if user:
                return user.username  # Return actual username for auth
        except ValidationError:
            pass

        # Check if input is phone
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if phone_pattern.match(contact_info):
            user = CustomUser.objects.filter(phone = contact_info).first()
            if user:
                return user.username # Return actual username for auth
        
        # Check if input is username
        user = CustomUser.objects.filter(username = contact_info).first()
        if user:
            return contact_info
        
        # If no matches found
        raise ValidationError("Invalid login credentials.")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({
            'atocomplete': 'current-password',
        })

class CustomSignupForm(SignupForm):
    # Add phone field to allauth's default signup form
    contact = forms.CharField(
        max_length=20,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone must be in international format (e.g., +1234567890)."
            ) 
        ],
        widget= forms.TextInput(attrs={"placeholder": "Phone (optional)"}),
    ) 

    username = forms.CharField(
        max_length= 30,
        validators= [MinLengthValidator(4)],
        widget= forms.TextInput(attrs={"placeholder": "Username(4-30 characters)"}),
    )
    email = forms.EmailField(
        required=False,
        widget= forms.EmailInput(attrs={"placeholder" : "Email (optional)"})
    )    


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone = cleaned_data.get("phone")

        if not (email or phone):
            raise forms.ValidationError("You must provide either an email or phone number.")
        return cleaned_data
    
    def save(self, request):
        user = super().save(request)
        user.phone = self.cleaned_data.get("phone")
        user.save()
        return user