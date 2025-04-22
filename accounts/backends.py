from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username =None, password = None, **kwargs):
        if username is None:
            return None
        
        username = username.lower() # Case insensitive lookup
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email__iexact=username) |  # Case insensative email
                Q(phone=username) 
            )
        except User.DoesNotExist:
             return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None