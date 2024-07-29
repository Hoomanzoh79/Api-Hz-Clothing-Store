from django.urls import path, include
from .views import index

app_name = "cloths"

urlpatterns = [
    path("api/v1/", include("cloths.api.v1.urls")),
    path("",index,name="index"),
]
