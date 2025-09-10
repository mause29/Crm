from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import obtener_embudo_ventas, ReporteVentas

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    embudo = obtener_embudo_ventas()
    ventas_por_usuario = ReporteVentas.objects.values('usuario__username').annotate(total=models.Sum('total_ventas'))
    return Response({
        "embudo": embudo,
        "ventas_por_usuario": list(ventas_por_usuario),
    })
