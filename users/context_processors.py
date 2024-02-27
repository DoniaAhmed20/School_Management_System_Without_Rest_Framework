from django.conf import settings

def set_auth_user_model(request):
    if request.path == '/login/':
        return {'AUTH_USER_MODEL': 'users.User'}
    else:
        return {'AUTH_USER_MODEL': settings.AUTH_USER_MODEL}
