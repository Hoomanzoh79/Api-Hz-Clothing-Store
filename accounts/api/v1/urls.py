from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

app_name = 'api-v1'

urlpatterns = [
    # signup
    path("registration/",views.RegistrationApiView.as_view(),name='registration'),
    # token login and logout
    path("token/login/",views.CustomAuthToken.as_view(),name="token-login"),
    path("token/logout/",views.DiscardAuthToken.as_view(),name="token-logout"),

    # jwt login 
    path("jwt/create/",views.CustomTokenObtainPairView.as_view(),name="jwt-create",),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    # change password
    path("password/change/",views.ChangePasswordApiView.as_view(),name='change-password'),
]