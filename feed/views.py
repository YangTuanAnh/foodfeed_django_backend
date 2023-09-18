from django.shortcuts import render
from posts.models import Post
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import  json

def timeline(request):
    if request.method=="GET":
        posts = Post.objects.order_by('-create_at')[:50]
        posts_json = [
            {
                "id": post.id,
                "user": post.user.id,
                "title": post.title,
                "body": post.body,
                "food": post.food.id,
                "rating": post.rating,
                "image_link": post.image_link,
                "username": post.user.username,
                "full_name": post.user.profile.full_name,
                "create_at": str(post.create_at),
            } for post in posts
        ]
        return JsonResponse(posts_json, status=200, safe=False)