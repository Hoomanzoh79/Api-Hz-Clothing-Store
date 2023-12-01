from django.urls import path,include
from .views import index_page

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path('index/',index_page,name='index'),
]