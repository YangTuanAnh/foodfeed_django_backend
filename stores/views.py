from django.shortcuts import render
from .models import Store
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def search_autocomplete(request):
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

        return JsonResponse(
            {'status': "success", 'results': serialized_results, 'count': len(results)},
            safe=False, status=200
        )
    else:
        return HttpResponse("Search")

@csrf_exempt
def stores(request, store_id):
    if request.method == "GET":
        try:
            store = Store.objects.get(id = store_id)
            return JsonResponse({"status": "success", 'result': store}, status=200)
        except Store.DoesNotExist:
            return JsonResponse({"status": f"Did not found store {store_id}", "result" : None}, status=404)
    
    elif request.method == "POST":
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')
        
        # check if any of the fields are empty
        if name == '' or address == '' or latitude == '' or longitude == '':
            return JsonResponse({"status": "Missing fields"}, status=400)
        
        # check if the store already exists
        store = Store.objects.filter(name=name, address=address, latitude=latitude, longitude=longitude)
        if store is not None:
            return JsonResponse({"status": "Store already exists"}, status=400)
        
        # create the store
        store = Store.objects.create(name=name, address=address, latitude=latitude, longitude=longitude)
        return JsonResponse({"status": "Created store " + str(store.id)}, status=200)
    
    elif request.method == "PUT":
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        latitude = request.POST.get('latitude', '')
        longitude = request.POST.get('longitude', '')
        
        # check if any of the fields are empty
        if name == '' or address == '' or latitude == '' or longitude == '':
            return JsonResponse({"status": "Missing fields"}, status=400)
        
        # check if the store not exists
        store = Store.objects.filter(name=name, address=address, latitude=latitude, longitude=longitude)
        if store is None:
            return JsonResponse({"status": "Store does not exist"}, status=400)
        
        # update the store
        store = Store.objects.filter(name=name, address=address, latitude=latitude, longitude=longitude).update(name=name, address=address, latitude=latitude, longitude=longitude)
        return JsonResponse({"status": "Updated store " + str(store.id)}, status=200)
    
    elif request.method == "DELETE":
        store = Store.objects.get(store_id)
        if store is None:
            return JsonResponse({"status": f"Did not found store {store_id}"}, status=404)
        else:
            store.delete()
            return JsonResponse({"status": "Deleted store " + str(store.id)}, status=200)
        
    else:
        return HttpResponse("Stores")