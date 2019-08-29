from django.urls import path
from apps.api.view import login


urlpatterns = [
    path('login/', login)
]