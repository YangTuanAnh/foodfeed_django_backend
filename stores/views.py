from django.shortcuts import render
from .models import Store
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')  # Get the search query from the request
        limit = int(request.GET.get('limit', 10))  # Get the number of results to display from the request
        
        # # Perform a search on stores by name and address
        # results = Store.objects.filter(
        #     Q(name__icontains=query) | Q(address__icontains=query)
        # )

        # fuzzy search
        threshold = 0.2
        results = Store.objects.similar_to(query, threshold)[:limit]

        # Serialize the results to JSON
        serialized_results = [
            {'name': store.name, 'address': store.address, 'latitude': store.latitude, 'longitude': store.longitude}
            for store in results
        ]

        return JsonResponse({'results': serialized_results})
    else:
        return HttpResponse("Search")

@csrf_exempt
def update(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id', '')
        if id == '':
            return JsonResponse({'status': 'Missing id'}, status=400)
        name = data.get('name', '')
        address = data.get('address', '')
        latitude = data.get('latitude', '')
        longitude = data.get('longitude', '')

        store = Store.objects.get(id=id)
        store.name = name
        store.address = address
        store.latitude = latitude
        store.longitude = longitude
        store.save()

        return JsonResponse({'status': f'Updated store {str(id)}'})
    else:
        return HttpResponse("Update")
    
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = data.get('id', '')
        if id == '':
            return JsonResponse({'status': 'Missing id'}, status=400)
        store = Store.objects.get(id=id)
        store.delete()
        return JsonResponse({'status': f'Deleted store {str(id)}'})
    else:
        return HttpResponse("Delete")
    
@csrf_exempt
def create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name', '')
        address = data.get('address', '')
        latitude = data.get('latitude', '')
        longitude = data.get('longitude', '')
        store = Store.objects.create(name=name, address=address, latitude=latitude, longitude=longitude)
        return JsonResponse({'status': f'Created store {str(store.id)}'})
    else:
        return HttpResponse("Create")
    
@csrf_exempt
def get(request):
    if request.method == 'GET':
        id = request.GET.get('id', '')
        if id == '':
            return JsonResponse({'status': 'Missing id'}, status=400)
        store = Store.objects.get(id=id)
        return JsonResponse({'name': store.name, 'address': store.address, 'latitude': store.latitude, 'longitude': store.longitude})
    else:
        return HttpResponse("Get")