from django.db import models
from clients.models import Client

class Contract(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    document_url = models.URLField()
    signed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
