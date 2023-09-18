from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import Post, Reaction
from food.models import Food
import json
from django.core import serializers
import re
import base64
from foodfeed_app.settings import STORAGE_URL, STORAGE_API_KEY, MEDIA_ROOT, BUCKET_NAME
from django.utils import timezone
import os
import io
from supabase import create_client

supabase = create_client(STORAGE_URL, STORAGE_API_KEY)
image_folder = os.path.join(MEDIA_ROOT, BUCKET_NAME)

def save_uploaded_file(uploaded_file, pdf_name, destination_path):
    # Step 0: Check if the destination path exists, if not, create it
    os.makedirs(destination_path, exist_ok=True)

    # Step 1: Access the file content
    file_content = uploaded_file.read()

    # Step 2: Choose a destination path (including filename)
    full_destination_path = os.path.join(destination_path, pdf_name)

    # Step 3: Write content to the file
    with open(full_destination_path, "wb") as destination_file:
        destination_file.write(file_content)

def remove_special_characters_and_replace_spaces(input_string):
    # Find the last period (.) in the string
    last_period_index = input_string.rfind('.')

    # Split the string into two parts: before and after the last period
    if last_period_index != -1:
        before_last_period = input_string[:last_period_index]
        after_last_period = input_string[last_period_index:]
    else:
        before_last_period = input_string
        after_last_period = ""

    # Remove special characters except for underscores in the "before" part
    cleaned_before_part = re.sub(r'[^a-zA-Z0-9\s_]', '', before_last_period)

    # Replace spaces with underscores in both parts
    cleaned_before_part = cleaned_before_part.replace(' ', '_')
    after_last_period = after_last_period.replace(' ', '_')

    # Concatenate the "before" and "after" parts with the last period
    cleaned_string = cleaned_before_part + '_' + str(timezone.now().timestamp()) + ".jpg"

    return cleaned_string

def uploadOntoS3(image_base64, image_name):
    image_name = remove_special_characters_and_replace_spaces(image_name)
    image_binary = base64.b64decode(image_base64)
    file_obj = io.BytesIO(image_binary)
    file_obj.seek(0)
    file = io.BufferedReader(file_obj)

    fileName = os.path.join(image_folder, image_name)
    save_uploaded_file(file, fileName, image_folder)
    
    upload=supabase.storage.from_(BUCKET_NAME).upload(image_name, file, {"content-type": "image/png"})
    
    os.remove(fileName)
    
    return f'{STORAGE_URL}/storage/v1/object/public/{BUCKET_NAME}/{image_name}'
    
# Create your views here.
@csrf_exempt
def posts(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    
    if request.method=="POST":
        data = json.loads(request.body)
                
        user = request.user
        title = re.sub(r'<.*?>', '', data.get("title"))
        body = re.sub(r'<.*?>', '', data.get("body"))
        if len(body)==0 or len(title)==0:
            messages.error(request, "Missing body or title")
            return JsonResponse({"status": "Missing body or title"}, status=302)
        
        rating = data.get("rating")
        
        image_base64 = data.get("image_base64")
        image_name = data.get("image_name")
        
        food_id = data.get("food_id")
        
        food = Food.objects.get(id=food_id)
        
        image_link = uploadOntoS3(image_base64, image_name)        
        
        post = Post.objects.create(user=user, body=body, rating=rating, title=title, food=food, image_link=image_link)
        
        return JsonResponse({"status": "Created post " + str(post.id)}, status="200")
        
    
    elif request.method=='GET':
        posts = Post.objects.filter(user=request.user)
        posts_json = serializers.serialize('json', posts)
        return JsonResponse(json.loads(posts_json), safe=False, status=200)

def post(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method=="GET":
        try:
            post = Post.objects.get(id=post_id)
            messages.success(request, f"Found post {post_id}")
            post_json = {
                "id": post.id,
                "user": post.user.id,
                "title": post.title,
                "body": post.body,
                "rating": post.rating,
                "image_link": post.image_link,
                "username": post.user.username,
                "full_name": post.user.profile.full_name,
                "create_at": str(post.create_at),
            }
            return JsonResponse(post_json, safe=False, status=200)
        except Post.DoesNotExist:
            messages.error(request, f"Did not found post {post_id}")
            return JsonResponse({"status": f"Did not found post {post_id}"}, status=404)
    if request.method=="DELETE":
        try:
            post = Post.objects.delete(id=post_id, user=request.user)
            messages.success(request, f"Deleted post {post_id}")
            return JsonResponse({"status": f"Deleted post {post_id}"}, status=200)
        except Post.DoesNotExist:
            messages.error(request, f"Did not found post {post_id}")
            return JsonResponse({"status": f"Did not found post {post_id}"}, status=404)
    
@login_required
@csrf_exempt
def reactions(request, post_id):
    try:
        post = Post.objects.get(id=post_id)

        if request.method=="GET":
            reactions = Reaction.objects.filter(post=post)
            users = [row.user.id for row in reactions]
            return JsonResponse({"count": len(users), "Users": users}, safe=False, status=200)
            
        elif request.method=='POST':
            existing_reaction = Reaction.objects.filter(user=request.user, post=post).first()
            if existing_reaction:
                existing_reaction.delete()
                return JsonResponse({"status": f"Deleted reaction from {post_id}"}, status=200) 
            else:
                reaction = Reaction(user=request.user, post=post)
                reaction.save()
                return JsonResponse({"status": str(reaction)}, status=200)
                
    except Post.DoesNotExist:
        messages.error(request, f"Did not found post {post_id}")
        return JsonResponse({"status": f"Did not found post {post_id}"}, status=404)
    
def food_reviews(request, food_id):
    if request.method=="GET":
        food = Food.objects.get(id=food_id)
        posts = Post.objects.filter(food=food)[:50]
        posts = [
            {
                "id": post.id,
                "user": post.user.id,
                "title": post.title,
                "body": post.body,
                "rating": post.rating,
                "image_link": post.image_link,
                "username": post.user.username,
                "full_name": post.user.profile.full_name,
                "create_at": str(post.create_at),
            }
            for post in posts
        ]

        return JsonResponse(posts, safe=False, status=200)