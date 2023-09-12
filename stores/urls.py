from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search),
    path("<int:store_id>/", views.stores),
]

