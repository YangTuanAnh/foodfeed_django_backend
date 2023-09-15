from django.urls import path
from . import views

urlpatterns = [
    path("search", views.search),
    path("search-autocomplete", views.search_autocomplete),
    path("<int:food_id>", views.food)
]