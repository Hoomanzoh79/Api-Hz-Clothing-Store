from django.urls import path
from . import views

app_name = 'api-v1'

urlpatterns = [
    # signup
    path("registration/",views.RegistrationApiView.as_view(),name='registration'),
    # token login and logout
    path("token/login/",views.CustomAuthToken.as_view(),name="token-login"),
    path("token/logout/",views.DiscardAuthToken.as_view(),name="token-logout"),
]