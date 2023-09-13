from django.db import models
from stores.models import Store

# Create your models here.
class Food(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(blank=False, max_length=255)
    store = models.ForeignKey(Store, to_field="id", on_delete=models.CASCADE)
    price = models.FloatField(blank=False, default=0)
    image_link = models.CharField(blank=False, max_length=255)
    
    def __str__(self):
        return self.name
    