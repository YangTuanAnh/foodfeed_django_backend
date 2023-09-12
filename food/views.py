from django.shortcuts import render
from .models import Food
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def create(request):
    if request.method == "POST":
        
