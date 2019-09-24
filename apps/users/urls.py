from django.urls import path
from rest_auth.views import UserDetailsView
from rest_framework.routers import DefaultRouter

from apps.users import views


router = DefaultRouter()
router.register(r'', views.UserDataForStaffViewSet, basename='user')

userpatterns = [
    path('me/', UserDetailsView.as_view()),
]

userpatterns += router.urls
