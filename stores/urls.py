from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.search),
    path("update/", views.update),
    path("delete/", views.delete),
    path("create/", views.create),
    path("get/", views.get),
]

