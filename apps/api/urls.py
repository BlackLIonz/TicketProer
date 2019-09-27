from django.urls import path, include
from rest_auth.registration.views import RegisterView
from rest_auth.views import LogoutView, LoginView

from apps.events.urls import eventpatterns
from apps.feedbacks.urls import reviewpatterns, commentpatterns
from apps.locations.urls import placepatterns, addresspatterns
from apps.subscriptions.urls import subscriptionpatterns
from apps.users.urls import userpatterns, organizationpatterns

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
    path('addresses/', include(addresspatterns)),
    path('organizations/', include(organizationpatterns)),
    path('comments/', include(commentpatterns)),
    path('subscriptions/', include(subscriptionpatterns)),
    path('reviews/', include(reviewpatterns)),
]
