class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    dominio = models.CharField(max_length=50, unique=True)

class Cliente(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
