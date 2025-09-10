# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from crm_project.settings import USER_ROLES

class User(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='sales')
