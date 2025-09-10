import hashlib
from django_cryptography.fields import encrypt

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    datos_sensibles = encrypt(models.TextField())  # Datos encriptados

# Logs de auditoría
class AuditLog(models.Model):
    usuario = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
