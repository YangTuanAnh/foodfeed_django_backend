from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import CustomUser as User
from .models import Profile, Friend
from .backends import EmailBackend
from django.db.models import Q
import json
from django.core import serializers
from posts.views import uploadOntoS3

# Create your views here.
@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Get form values
        data = json.loads(request.body)
        full_name = data.get('full_name')
        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        password2 = data.get('password2')

        print(full_name, username, email, phone_number, password, password2)
        
        # Check if passwords match
        if password == password2:
        # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
            
                return JsonResponse(
                    {"status": 'That username is taken'},
                    status=302
                )
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return JsonResponse(
                        {"status": 'That email is being used'},
                        status=302
                    )
                else:
                # Looks good
                    profile = Profile.objects.create(full_name=full_name)
                    user = User.objects.create_user(username=username, password=password,email=email, phone_number=phone_number, profile=profile)
                    # Login after register
                    auth.login(request, user, 'users.backends.EmailBackend')
                    # messages.success(request, 'You are now logged in')
                    
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return JsonResponse(
                        {"status": 'You are now registered and can log in'},
                        status=200
                    )
                    # return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return JsonResponse(
                {"status": 'Passwords do not match'},
                status=400
            )
    else:
        print("Register")
        return HttpResponse("Register")
    
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        user = auth.authenticate(request=request, email=email, password=password)

        if user is not None:
            #debug here
            print("user is not none")
            
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return JsonResponse(
                {"status": "You are now logged in"},
                status=200
            )
        else:
            print("user is none")
            messages.error(request, 'Invalid credentials')

            return JsonResponse(
                {"status": "Invalid credentials"},
                status=403
            )
    else: return HttpResponse("Login")
    
@csrf_exempt
def logout(request):
    # if not request.user.is_authenticated:
    #     return JsonResponse(
    #         {"status": "Unauthenticated"},
    #         status=400
    #     )
    if request.method=="POST":
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return JsonResponse(
            {"status": "You are now logged out"},
            status=200
        )
    else: return HttpResponse("Logout")
        
@csrf_exempt
def profile(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method=="PUT":
        data = json.loads(request.body)
        profile = request.user.profile
        profile.full_name, profile.bio, profile.avatar_base64, profile.avatar_filename = data.get('full_name'), data.get('bio'), data.get('avatar_base64'), data.get('avatar_filename')
        profile.avatar = uploadOntoS3(image_base64=profile.avatar_base64, image_name=profile.avatar_filename)
        profile.save()
        return JsonResponse({"status": "Updated profile"}, status=200)
    elif request.method=="GET":
        profile = request.user.profile
        return JsonResponse({
            "full_name": profile.full_name,
            "bio": profile.bio,
            "avatar": profile.avatar
        }, status=200)
    
def get_user(request, user_id):
    if request.method=="GET":
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
            #messages.success(f"Found user {user_id}")
            return JsonResponse({
                "full_name": profile.full_name,
                "bio": profile.bio,
                "avatar": profile.avatar
            }, status=200)
        except User.DoesNotExist:
            #messages.error(f"User {user_id} does not exist")
            return JsonResponse({"status": f"User {user_id} does not exist"}, status=404)

def friends(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method=="GET":
        user_friends = Friend.objects.filter(user_from=request.user).values_list('user_to', flat=True)
       
        users = []
        for user_id in user_friends:
            user = User.objects.get(id = user_id)
            users.append({"username" : user.username, "id": user_id})
    
        print(users)

        return JsonResponse(users, status=200, safe = False)

        friends_json = serializers.serialize('json', list(user_friends))
        
        #print(user_friends)
        #print(type(user_friends))

        return JsonResponse(user_friends, status=200, safe = False)

@csrf_exempt
def make_friend(request, user_id):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "Unauthenticated"},
            status=400
        )
    if request.method=="GET":
        user = User.objects.get(id=user_id)
        user_friends = Friend.objects.filter(user_from=user).values_list('user_to', flat=True)
            
        friends_json = serializers.serialize('json', user_friends)
        
        return JsonResponse(friends_json, status=200)
    elif request.method=="POST":
        user1 = User.objects.get(id=request.user.id)
        user2 = User.objects.get(id=user_id)
        
        try:
            exists = Friend.objects.get(user_from=user1, user_to=user2)
            exists.delete()
            print("This is THE POST " + f"Removed friendship between {user1.id} and {user2.id}")
            return JsonResponse(f"Removed friendship between {user1.id} and {user2.id}", status=200, safe = False)
        except Friend.DoesNotExist:
            friendship = Friend(user_from=user1, user_to=user2)
            friendship.save()
            return JsonResponse(f"Added friendship between {user1.id} and {user2.id}", status=200, safe = False)
        
def suggestions(request):
    if request.method=="GET":
        suggest_users = User.objects.exclude(id=request.user.id)

        friends = Friend.objects.filter(user_from=request.user).values_list("user_to")

        for user in list(friends):
            suggest_users = suggest_users.exclude(id = user[0])
            print(":", user[0])

        #suggest_users = suggest_users.exclude(user_to__in=list(friends))
        suggest_users = suggest_users.order_by('?')[:5]

        users_json = serializers.serialize('json', suggest_users)
        return JsonResponse(json.loads(users_json), status=200, safe = False)