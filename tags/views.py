from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Tag
from stores.models import Store
from django.db.models import F
from geopy.distance import geodesic
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def tags(request):
    if request.method=="GET":
        query = request.GET.get('query', '')
        tag = Tag.objects.get(name=query)
        if tag.DoesNotExist():
            return JsonResponse({"status": "Tag does not exist"}, status=404)
        return JsonResponse({
            "id": tag.id,
            "name": tag.name,
            "store_id": tag.store
        }, status=200)
    elif request.method=="POST":
        query = request.POST.get('query', '')
        latitude = float(request.POST.get('latitude', '0'))
        longitude = float(request.POST.get('longitude', '0'))
        try:
            tag = Tag.objects.get(title=query)
            return JsonResponse({"status": "Tag does exist"}, status=302)
        
        except Tag.DoesNotExist:
            stores = Store.objects.all()
            nearest_store = None
            min_distance = float("inf")

            for store in stores:
                store_latitude = store.latitude
                store_longitude = store.longitude
                
                if (store_latitude is None or store_longitude is None):
                    continue
                if (abs(store_latitude)>90 or abs(store_longitude)>180):
                    continue
                
                distance = geodesic((latitude, longitude), (store_latitude, store_longitude)).km
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_store = store
            
            new_tag = Tag.objects.create(title=query, store=nearest_store)
            new_tag.save();
            return JsonResponse({"status": f"#{query} was created with store {str(nearest_store)}"}, status=200)