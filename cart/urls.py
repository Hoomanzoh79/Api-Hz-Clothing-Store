from django.urls import path, include

app_name = "cart"

urlpatterns = [
    path("api/v1/", include("cart.api.v1.urls")),
]
