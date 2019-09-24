from rest_framework.routers import DefaultRouter

from apps.feedbacks import views


review_router = DefaultRouter()

review_router.register(r'', views.ReviewViewSet, basename='review')

reviewpatterns = review_router.urls
