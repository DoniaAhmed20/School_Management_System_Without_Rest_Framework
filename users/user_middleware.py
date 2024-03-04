# # middleware.py
# from django.conf import settings

# class SetAuthUserModelMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.path == '/login/':
#             settings.AUTH_USER_MODEL = 'users.User'
#         # else:
#         #     settings.AUTH_USER_MODEL = 'your_default_user_model'

#         response = self.get_response(request)
#         return response


from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated and request.path == reverse('my_profile'):
            messages.error(request, 'You must be logged in to view this page.')
            return redirect('login')  # Redirect to the login page
        return response

