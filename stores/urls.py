from django.urls import path
from . import views

urlpatterns = [
    path("search-autocomplete/", views.search_autocomplete),
    path("<int:store_id>/", views.stores),
]

