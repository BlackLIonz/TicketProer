from django.urls import re_path, path, include
from rest_auth.registration.views import RegisterView, LoginView


authpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view())
]


urlpatterns = [
    path(r'auth/', include(authpatterns)),
]