from django.shortcuts import render
from posts.models import Post
from django.core import serializers
from django.http import HttpResponse, JsonResponse

# Create your views here.
def timeline(request):
    if request.method=="GET":
        posts = Post.objects.order_by('-create-at')[:50]
        posts_json = serializers.serialize('json', posts)
        return JsonResponse(posts_json, status=200)