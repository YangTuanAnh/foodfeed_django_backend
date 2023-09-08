from django.shortcuts import render
from .models import Store
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

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

# def test_connection(request):
#     # Retrieve the first 10 stores from the database
#     stores = Store.objects.all()[:10]

#     # Serialize the store data to JSON
#     serialized_stores = [
#         {
#             'name': store.name,
#             'address': store.address,
#             'latitude': store.latitude,
#             'longitude': store.longitude,
#         }
#         for store in stores
#     ]

#     return JsonResponse({'stores': serialized_stores})