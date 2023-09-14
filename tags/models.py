from django.db import models
from stores.models import Store

# Create your models here.

class Tag(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    title = models.CharField(max_length=255, blank=False)
    store = models.ForeignKey(Store, to_field="id", on_delete=models.CASCADE)