from . import views
from rest_framework_nested import routers

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("orders", views.OrderViewSet, basename="orders")

urlpatterns = router.urls 