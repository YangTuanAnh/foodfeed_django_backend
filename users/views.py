from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import CustomUser as User
from .models import Profile
import json

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
                    auth.login(request, user)
                    messages.success(request, 'You are now logged in')
                    return JsonResponse(
                        {"status": 'You are now logged in'},
                        status=200
                    )
                    # user.save()
                    # messages.success(request, 'You are now registered and can log in')
                    # return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return JsonResponse(
                {"status": 'Passwords do not match'},
                status=400
            )
    else:
        return HttpResponse("Register")
    
@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return JsonResponse(
                {"status": "You are now logged in"},
                status=200
            )
        else:
            messages.error(request, 'Invalid credentials')
            return JsonResponse(
                {"status": "Invalid credentials"},
                status=403
            )
    else: return HttpResponse("Login")
    
@csrf_exempt
@login_required
def logout(request):
    if request.method=="POST":
        auth.logout(request)
        messages.error(request, "You are now logged out")
        return JsonResponse(
            {"status": "You are now logged out"},
            status=200
        )
    else: return HttpResponse("Logout")
        
@csrf_exempt
@login_required
def profile(request):
    if request.method=="PUT":
        data = json.loads(request.body)
        profile = request.user.profile
        profile.full_name, profile.bio, profile.avatar = data.get('full_name'), data.get('bio'), data.get('avatar')
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
            messages.success(f"Found user {user_id}")
            return JsonResponse({
                "full_name": profile.full_name,
                "bio": profile.bio,
                "avatar": profile.avatar
            }, status=200)
        except User.DoesNotExist:
            messages.error(f"User {user_id} does not exist")
            return JsonResponse({"status": f"User {user_id} does not exist"}, status=404)

