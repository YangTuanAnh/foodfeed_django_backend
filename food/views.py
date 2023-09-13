from django.shortcuts import render
from .models import Food
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def food(request, food_id):
    if request.method == "GET":
        food = Food.objects.get(food_id)
        if food is None:
            return JsonResponse({"status": f"Did not found food {food_id}"}, status=404)
        else:
            return JsonResponse({"status": "success", 'results': food}, status=200)
        
    elif request.method == "POST":
        name = request.POST.get('name', '')
        store_id = int(request.POST.get('store_id', ''))
        price = float(request.POST.get('price', ''))

        # TODO: add image link
        
        # check if all fields are empty
        if name == '' or store_id == '' or price == '':
            return JsonResponse({"status": "error", "message": "All fields must be filled"}, status=400)
        
        # check if store is not exists
        store = Store.objects.get(store_id)
        if store is None:
            return JsonResponse({"status": "error", "message": "Store does not exists"}, status=400)
        
