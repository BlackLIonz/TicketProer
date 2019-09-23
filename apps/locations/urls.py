from rest_framework.routers import DefaultRouter

from apps.locations import views


router = DefaultRouter()
router.register(r'', views.PlaceViewSet, basename='place')

placepatterns = router.urls
