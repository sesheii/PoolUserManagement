from django.contrib import admin
from django.urls import path
from . import views as api_views

urlpatterns = [
    # path('getUsers/', api_views.getUsers),
    # path('getUsers/<int:user_id>', api_views.getUser),
    # path('addUser/', api_views.addUser),
    path('Users/', api_views.CreateUsers),
    path('Users/<int:user_id>', api_views.Users),

]
