from django.http import HttpResponseForbidden
from crm.models import Empresa

class MultiTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        dominio = request.get_host().split(':')[0]
        try:
            request.empresa = Empresa.objects.get(dominio=dominio)
        except Empresa.DoesNotExist:
            return HttpResponseForbidden("Empresa no encontrada")
        return self.get_response(request)
