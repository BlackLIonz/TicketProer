from django.urls import re_path, path, include
from rest_auth.registration.views import VerifyEmailView, RegisterView


authpatterns = [
    path('registration/', RegisterView.as_view()),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
            name='account_confirm_email'),
]


urlpatterns = [
    path(r'auth/', include(authpatterns)),
]