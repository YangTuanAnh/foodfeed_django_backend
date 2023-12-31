from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts),
    path("<int:post_id>", views.post),
    path("reactions/<int:post_id>", views.reactions),
    path("food/<int:food_id>", views.food_reviews)
]

