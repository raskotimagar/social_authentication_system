from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        process = request.GET.get('process')
        if process == 'login':
            email = sociallogin.account.extra_data.get('email')
            if email:
                # Check if the user exists in the database
                user_exists = self._user_exists(email)
                if not user_exists:
                    messages.error(request, "No account found with this Google account. Please sign up first.")
                    raise ImmediateHttpResponse(HttpResponseRedirect(reverse('account_login')))
                else:
                    try:
                        email_address = EmailAddress.objects.get(email=email)
                        if not email_address.verified:
                            raise ImmediateHttpResponse(HttpResponseRedirect(reverse('account_email_verification_sent')))
                    except EmailAddress.DoesNotExist:
                        pass
    
    def _user_exists(self, email):
        User = get_user_model()
        return User.objects.filter(email = email).exists()

        
    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        # Map google data to  your CustomUser fields
        user.email = sociallogin.account.extra_data.get('email')
        user.username = sociallogin.account.extra_data.get('name', 'user') # Generate unique username
        user.name = sociallogin.account.extra_data.get('name', '')
        return user