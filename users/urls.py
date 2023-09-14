from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login,),
    path("register", views.register,),
    path("logout", views.logout,),
    path("profile", views.profile,),
    path("profile/<int:user_id>", views.get_user,),
    path("friends", views.friends),
    path("friends/<int:user_id>", views.make_friend),
    path("friends/pending", views.friends_pending)
]