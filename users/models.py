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
        default="https://ppbcpbhpzrhbhikjrtbb.supabase.co/storage/v1/object/public/images/ntmcuitluhlo_1694650728.778543",
    )
    def __str__(self):
        return self.id
    
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    profile = models.ForeignKey(Profile, to_field="id", on_delete=models.CASCADE, default=datetime.now().timestamp())

class Friend(models.Model):
    user_from = models.ForeignKey(CustomUser, to_field="id", on_delete=models.CASCADE, related_name="user_from")
    user_to = models.ForeignKey(CustomUser, to_field="id", on_delete=models.CASCADE, related_name="user_to")
    #accepted = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user_from', 'user_to')
        
    def __str__(self):
        return f"{self.user1} and {self.user2}"