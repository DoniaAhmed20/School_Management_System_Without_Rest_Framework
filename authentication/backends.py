# authentication/backends.py

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class CustomUserModelBackend(ModelBackend):
    """
    Authentication backend that dynamically switches between the default
    user model and custom user model.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if getattr(request, 'admin_auth', False):
            # Admin authentication, use default user model
            user_model = get_user_model()
        else:
            # Regular user authentication, use custom user model
            from users.models import User
            user_model = User
        
        try:
            user = user_model.objects.get(username=username)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None