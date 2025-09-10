# apps/opportunities/models.py

from django.db import models
from apps.clients.models import Client
from apps.users.models import User

STAGES = (
    ('prospect', 'Prospect'),
    ('negotiation', 'Negotiation'),
    ('closed_won', 'Closed Won'),
    ('closed_lost', 'Closed Lost'),
)

class Opportunity(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=255)
    stage = models.CharField(max_length=50, choices=STAGES, default='prospect')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    probability = models.IntegerField(default=0)  # 0-100%
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='opportunities')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
