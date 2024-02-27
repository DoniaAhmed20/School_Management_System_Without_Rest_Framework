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
