from django.db import models
from django.contrib.auth.models import AbstractUser

# --- Usuarios con roles ---
class Usuario(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('VENDEDOR', 'Vendedor'),
        ('CLIENTE', 'Cliente'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='CLIENTE')

# --- Clientes ---
class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=50, blank=True)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# --- Oportunidades ---
class Oportunidad(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, default="NUEVO")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.cliente.nombre}"

# --- Tareas ---
class Tarea(models.Model):
    oportunidad = models.ForeignKey(Oportunidad, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=50, default="PENDIENTE")
    fecha_vencimiento = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# --- Facturas ---
class Factura(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default="PENDIENTE")
    fecha = models.DateTimeField(auto_now_add=True)
    paypal_order_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Factura #{self.id} - {self.cliente.nombre}"
