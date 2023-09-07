from django.db import models
from users.models import CustomUser as User
from django.utils import timezone

# Create your models here.
    
class Store(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    avg_rating = models.FloatField(default=0)
    image_link = models.CharField(max_length=255)

    def __str__(self):
        return self.name