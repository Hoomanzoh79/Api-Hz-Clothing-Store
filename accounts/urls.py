from django.urls import path, include
from .views import index_page

app_name = "accounts"

urlpatterns = [
    # basic auth
    path("", include("django.contrib.auth.urls")),
    # index
    path("index/", index_page, name="index"),
    path("api/v1/", include("accounts.api.v1.urls")),
]
