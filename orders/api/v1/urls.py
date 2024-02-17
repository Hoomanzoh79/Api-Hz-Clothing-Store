from . import views
from rest_framework_nested import routers

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("orders", views.OrderViewSet, basename="order")
order_items_router = routers.NestedDefaultRouter(router,"orders",lookup="order")
order_items_router.register("items",views.OrderItemViewSet,basename="order-items")

urlpatterns = router.urls + order_items_router.urls