from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = "api-v1"

router = DefaultRouter()
router.register("cart", views.CartViewSet, basename="cart")

urlpatterns = router.urls