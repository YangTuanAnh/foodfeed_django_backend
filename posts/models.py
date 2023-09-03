from django.db import models
from users.models import CustomUser as User
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE, default=timezone.now().timestamp())
    title = models.CharField(max_length=255, blank=False)
    body = models.TextField(blank=False)
    rating = models.IntegerField(default=1)
    image_link = models.CharField(max_length=255)
    create_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title
    
class Reaction(models.Model):
    post = models.ForeignKey(Post, to_field="id", on_delete=models.CASCADE)
    user = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'post')  # Ensure each user can react to a post only once

    def __str__(self):
        return f'{self.user.username} reacted to {self.post.title}'