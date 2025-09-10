# Ejemplo de protección CSRF, XSS, SQL Injection básica
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

class SecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Validar CSRF
        if request.method == "POST" and not request.META.get('CSRF_COOKIE'):
            return HttpResponseForbidden("CSRF token missing")
