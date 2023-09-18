from django.shortcuts import render
from posts.models import Post
from django.core import serializers
from django.http import HttpResponse, JsonResponse
import  json

def timeline(request):
    if request.method=="GET":
        posts = Post.objects.order_by('-create_at')[:50]
        posts_json = serializers.serialize('json', posts)
        return JsonResponse(json.loads(posts_json), status=200, safe=False)