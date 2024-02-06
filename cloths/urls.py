from django.urls import path, include
from .views import HelloPageView

app_name = "cloths"

urlpatterns = [
    path("api/v1/", include("cloths.api.v1.urls")),
    path("hello/",HelloPageView.as_view(),name="hello"),
]
