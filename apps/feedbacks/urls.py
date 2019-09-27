from rest_framework.routers import DefaultRouter

from apps.feedbacks import views

review_router, comment_router = DefaultRouter(), DefaultRouter()

review_router.register(r'', views.ReviewViewSet, basename='review')
comment_router.register(r'', views.CommentViewSet, basename='comments')

reviewpatterns = review_router.urls
commentpatterns = comment_router.urls
