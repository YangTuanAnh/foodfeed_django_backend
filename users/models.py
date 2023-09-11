# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import datetime

class Profile(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    full_name = models.CharField(max_length=255, blank=False)
    bio = models.CharField(max_length=255, blank=True)
    avatar = models.CharField(
        max_length=255,
        default="https://storage.googleapis.com/avatar-a0439.appspot.com/avatar.png",
    )
    def __str__(self):
        return self.id
    
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    profile = models.ForeignKey(Profile, to_field="id", on_delete=models.CASCADE, default=datetime.now().timestamp())
