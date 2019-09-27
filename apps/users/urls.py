from django.urls import path
from rest_auth.views import UserDetailsView
from rest_framework.routers import DefaultRouter

from apps.subscriptions.views import SubscriptionViewSet
from apps.users import views


router = DefaultRouter()
router.register(r'', views.UserDataForStaffViewSet, basename='user')

userpatterns = [
    path('me/', UserDetailsView.as_view()),
    path('me/events/', views.UserEventsViewSet.as_view({'get': 'list'})),
    path('me/events/<str:event_id>/detailed/', views.UserEventsViewSet.as_view({'get': 'retrieve'})),
    path('me/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
]

userpatterns += router.urls

organizationpatterns = [
    path('', views.OrganizationsViewSet.as_view({'get': 'list'})),
    path('<str:organization_id>/', views.OrganizationsViewSet.as_view({'get': 'retrieve'})),
    path('<str:organization_id>/detailed/', views.OrganizationsViewSet.as_view({'get': 'detailed'})),
]
