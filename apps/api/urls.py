from django.urls import path
from apps.api.view import login, logout, register


urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
]
