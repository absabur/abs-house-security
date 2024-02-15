from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HouseOwner(models.Model):
    name = models.CharField(max_length=40)
    password_1 = models.CharField(max_length=20)
    password_2 = models.CharField(max_length=20)
    unlock = models.BooleanField(default=False)
    attempt = models.IntegerField(default=3)
