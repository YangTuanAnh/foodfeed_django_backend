from django.db import models
from users.models import CustomUser as User
from django.utils import timezone
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

# Create your models here.
    
class StoreManager(models.Manager):
    def similar_to(self, query, threshold):
        return self.annotate(
            name_similarity=TrigramSimilarity('name', query),
            address_similarity=TrigramSimilarity('address', query),
        ).filter(
            Q(name_similarity__gt=threshold) | Q(address_similarity__gt=threshold)
        ).order_by('-name_similarity', '-address_similarity')

# class StoreManager(models.Manager):
#     def similar_to(self, query, threshold):
#         return self.annotate(
#             similarity = TrigramSimilarity('name', query),
#         ).filter(similarity__gt=threshold).order_by('-similarity')

class Store(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    avg_rating = models.FloatField(default=0)
    image_link = models.CharField(max_length=255)

    objects = StoreManager()

    def __str__(self):
        return self.name
