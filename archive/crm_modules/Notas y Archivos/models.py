class Nota(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="notas")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Archivo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="archivos")
    archivo = models.FileField(upload_to='archivos_clientes/')
    descripcion = models.CharField(max_length=255, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)
