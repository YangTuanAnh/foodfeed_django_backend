from django.urls import path
from . import views

urlpatterns = [
    path("", views.posts),
    path("<int:post_id>", views.post),
    path("search", views.search),
    path("reactions/<int:post_id>", views.reactions)
]

