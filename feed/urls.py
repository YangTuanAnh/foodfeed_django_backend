from django.urls import path
from . import views

urlpatterns = [
    path("timeline", views.timeline,),

]
