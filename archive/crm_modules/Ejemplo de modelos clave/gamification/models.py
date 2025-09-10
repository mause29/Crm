from django.db import models
from users.models import User

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    date_earned = models.DateTimeField(auto_now_add=True)
