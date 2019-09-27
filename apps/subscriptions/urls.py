from rest_framework.routers import DefaultRouter

from apps.subscriptions import views


router = DefaultRouter()
router.register('', views.SubscriptionViewSet, basename='subscriptions')

subscriptionpatterns = router.urls
