from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_employee = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True, null=True)