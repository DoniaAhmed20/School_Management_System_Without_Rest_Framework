from django.utils.deprecation import MiddlewareMixin

class AdminAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware to set a flag in request context indicating admin authentication.
    """

    def process_request(self, request):
        if request.path.startswith('/admin/'):
            request.admin_auth = True
        else:
            request.admin_auth = False
