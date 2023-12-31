from django.shortcuts import render
from .models import Food, Store
from posts.models import Post
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from posts.views import uploadOntoS3
from geopy.distance import geodesic
import json
from django.db.models.functions import Length
from foodfeed_app.settings import REDIS_CONNECTION
import re
# Create your views here.
@csrf_exempt
def food(request, food_id):
    if request.method == "GET":
        food = Food.objects.get(id=food_id)
        if food is None:
            return JsonResponse({"status": f"Did not found food {food_id}"}, status=404)
        else:
            # serialize the food object to JSON
            food = {'id': food.id,
                    'name': food.name,
                    'store_id': food.store.id,
                    'price': food.price,
                    'image_link': food.image_link,}
            return JsonResponse({"status": "success", 'results': food}, status=200)
        
    elif request.method == "POST":
        data = json.loads(request.body)

        name = data.get('name', '')
        store_id = int(data.get('store_id', ''))
        price = float(data.get('price', ''))
        image_base64 = data.get('image_base64', '')
        image_name = data.get('image_name', '')
        
        # check if all fields are empty
        if name == '' or store_id == '' or price == '' or image_base64 == '' or image_name == '':
            return JsonResponse({"status": "error", "message": "All fields must be filled"}, status=400)
        
        # check if store is not exists
        store = Store.objects.get(store_id)
        if store is None:
            return JsonResponse({"status": "error", "message": "Store does not exists"}, status=400)

        image_link = uploadOntoS3(image_base64, image_name)

        food = Food(name=name, store=store_id, price=price, image_link=image_link)
        food.save()

        return JsonResponse({"status": "success", "message": f"Added food {food.id}"}, status=200)
    
    elif request.method == "PUT":
        food = Food.objects.get(id=food_id)
        if food is None:
            return JsonResponse({"status": "error", "message": "Food does not exists"}, status=400)
        
        data = json.loads(request.body)

        name = data.get('name', '')
        store_id = int(data.get('store_id', ''))
        price = float(data.get('price', ''))
        image_base64 = data.get('image_base64', '')
        image_name = data.get('image_name', '')
        
        # check if all fields are empty
        if name == '' and store_id == '' and price == '' and image_base64 == '' and image_name == '':
            return JsonResponse({"status": "error", "message": "At least one fields must be filled"}, status=400)
        
        # check if store is not exists
        store = Store.objects.get(store_id)
        if store is None:
            return JsonResponse({"status": "error", "message": f"Store {store_id} does not exists"}, status=400)

        # Update each field if it is not empty
        if name != '':
            food.name = name
        if store_id != '':
            food.store = store_id
        if price != '':
            food.price = price
        if image_base64 != '' and image_link != '':
            image_link = uploadOntoS3(image_base64, image_name)
            food.image_link = image_link
        
        food.save()

        return JsonResponse({"status": "success", "message": f"Updated food {food.id}"}, status=200)
    
    elif request.method == "DELETE":
        food = Food.objects.get(id=food_id)
        if food is None:
            return JsonResponse({"status": "error", "message": f"Food {food_id} does not exists"}, status=400)

        food.delete()

        return JsonResponse({"status": "success", "message": f"Food {food_id} deleted successfully"}, status=200)
    
    else:
        return HttpResponse("Food", status=200)
    
DEFAULT_LINK="https://images.foody.vn/default/s120x120/shopeefood-deli-dish-no-image.png"
def search(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        offset = int(request.GET.get('offset', '0'))
        limit = int(request.GET.get('limit', '10'))
        latitude = float(request.GET.get('latitude', '0'))
        longitude = float(request.GET.get('longitude', '0'))
        distance = float(request.GET.get('distance', '0'))

        
        if query == '':
            return JsonResponse({"status": "error", "message": "Query must be filled"}, status=400)
        
        foods = Food.objects.filter(name__contains=query)[:50]

        debug = True

        if(debug):
            limit = 10
            offset = 0

        if debug or (latitude != 0 and longitude != 0 and distance != 0):
            filtered_foods = []
            for food in foods:

                if(len(filtered_foods) >= offset+limit):
                    break

                store = Store.objects.get(id=food.store.id)
                review = Post.objects.filter(food=food.id).order_by('create_at').first()
                if store:
                    food_distance = geodesic((latitude, longitude), (store.latitude, store.longitude)).km
                    if debug or (food_distance <= distance):
                        #filtered_foods.append({"food": food, "review": review})
                        if review:
                            filtered_foods.append({
                                "food": {
                                    "id": food.id,
                                    "name": food.name,
                                    "store": food.store.id,
                                    "price": food.price,
                                    "image_link": food.image_link
                                },
                                "review": {
                                    "id": review.id,
                                    "user": review.user.id,
                                    "title": review.title,
                                    "body": review.body,
                                    "food": review.food.id,
                                    "rating": review.rating,
                                    "image_link": review.image_link,
                                    "username": review.user.username,
                                    "full_name": review.user.profile.full_name,
                                    "create_at": review.create_at
                                }
                            })
                        else:
                            filtered_foods.append({
                                "food": {
                                    "id": food.id,
                                    "name": food.name,
                                    "store": food.store.id,
                                    "price": food.price,
                                    "image_link": food.image_link
                                },
                                "review": None
                            })

            results = filtered_foods[offset:offset+limit]
        else:
            results = foods[offset:offset+limit]

        l, r = 0, len(filtered_foods)-1
        while l<r:
            if filtered_foods[r]["food"]["image_link"]!=DEFAULT_LINK and filtered_foods[l]["food"]["image_link"]==DEFAULT_LINK:
                filtered_foods[l], filtered_foods[r] = filtered_foods[r], filtered_foods[l]
            if filtered_foods[l]["food"]["image_link"]!=DEFAULT_LINK:
                l+=1
            if filtered_foods[r]["food"]["image_link"]==DEFAULT_LINK:
                r-=1
                
                
        # print(query)
        # print(results)

        # Serialize the results to JSON, remember checking none and not make object to string
        
        #serialized_results = json.dumps(filtered_results, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        #serialized_results = serializers.serialize('json', filtered_foods)
        #print(serialized_results)
        return JsonResponse({"status": "success", "results": filtered_foods}, status=200)

def search_autocomplete(request):
    if request.method == "GET":
        query = request.GET.get('query', '')
        limit = int(request.GET.get('limit', '10'))
        
        query = re.sub(r'^\s+$', '', query)
        if len(query)<3:
            return JsonResponse({"status": "error", "results": []}, status=200)
        
        results = REDIS_CONNECTION.zrangebylex("autocomplete", "[" + query, "[" + query + "\xff", start=0, num=limit)

        results = [re.sub(r'\s+', ' ', re.sub(r'[^\s\w\dÀ-ÿ]+', '', result.decode("utf-8"))).strip() for result in results]
        
        results = sorted(results, key=lambda x: len(x))
        
        results = results[:limit]
        
        return JsonResponse({"status": "success", "results": results}, status=200)
    else:
        return HttpResponse("Autocomplete", status=200)