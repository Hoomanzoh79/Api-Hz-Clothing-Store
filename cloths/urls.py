from django.urls import path, include

app_name = "cloths"

urlpatterns = [
    path("api/v1/", include("cloths.api.v1.urls")),
]
