from django.db import models

class Invoice(models.Model):
    client_name = models.CharField(max_length=200)
    client_email = models.EmailField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client_name} - {self.amount} {self.currency}'
