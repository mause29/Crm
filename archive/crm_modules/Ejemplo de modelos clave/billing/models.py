from django.db import models
from clients.models import Client

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="USD")
    paid = models.BooleanField(default=False)
    paypal_transaction_id = models.CharField(max_length=255, blank=True)
    due_date = models.DateField()
