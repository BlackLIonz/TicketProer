from django.urls import path, include
from rest_auth.registration.views import RegisterView
from rest_auth.views import LogoutView, LoginView

from apps.locations.urls import placepatterns
from apps.events.urls import eventpatterns
from apps.users.urls import userpatterns


app_name = 'api'


authpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]

urlpatterns = [
    path('auth/', include(authpatterns)),
    path('users/', include(userpatterns)),
    path('places/', include(placepatterns)),
    path('events/', include(eventpatterns)),
]
