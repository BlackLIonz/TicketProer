from rest_framework.routers import DefaultRouter

from apps.locations import views

place_router = DefaultRouter()
address_router = DefaultRouter()

place_router.register(r'', views.PlaceViewSet, basename='place')
address_router.register(r'', views.AddressViewSet, basename='address')

placepatterns = place_router.urls
addresspatterns = address_router.urls
