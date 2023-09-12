from django.urls import path
from . import views

urlspatterns = [
    path("search/", views.search),
    path("search-autocomplete/", views.search_autocomplete),
    path("create/", views.create),
    path("get/", views.get),
    path("update/", views.update),
    path("delete/", views.delete),
]