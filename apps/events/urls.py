from rest_framework.routers import DefaultRouter

from apps.events import views


router = DefaultRouter()
router.register('', views.EventViewSet, basename='events')

eventpatterns = router.urls
