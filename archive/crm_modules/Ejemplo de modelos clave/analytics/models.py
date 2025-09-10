from django.db import models
from clients.models import Client
from opportunities.models import Opportunity

class KPI(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
    date = models.DateField(auto_now_add=True)
