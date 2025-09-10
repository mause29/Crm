from django.db import models
from django.contrib.auth.models import User
from crm.models import Cliente, Oportunidad

class ReporteVentas(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total_ventas = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Reporte {self.usuario.username} {self.fecha_inicio} - {self.fecha_fin}"

# Función para generar embudo de ventas
def obtener_embudo_ventas():
    etapas = ['Prospecto', 'En negociación', 'Cerrado']
    embudo = {}
    for etapa in etapas:
        count = Oportunidad.objects.filter(etapa=etapa).count()
        embudo[etapa] = count
    return embudo
