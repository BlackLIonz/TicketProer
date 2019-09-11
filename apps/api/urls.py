from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter
from rest_auth.registration.views import RegisterView
from rest_auth.views import LogoutView, LoginView
from apps.events import views as event_views
from apps.locations import views as location_views
from apps.users.urls import userpatterns

app_name = "api"

authpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]

router = DefaultRouter()
router.register(r'events', event_views.EventViewSet, basename='events')
router.register(r'places', location_views.PlaceViewSet, basename='place')

urlpatterns = [
    path(r'auth/', include(authpatterns)),
    path(r'user/', include(userpatterns))
]

urlpatterns += router.urls
