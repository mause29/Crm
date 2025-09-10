from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    two_factor_enabled = models.BooleanField(default=False)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, null=True)
