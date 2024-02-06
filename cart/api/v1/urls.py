from . import views
from rest_framework_nested import routers

app_name = "api-v1"

router = routers.DefaultRouter()
router.register("cart", views.CartViewSet, basename="cart")

cart_items_router = routers.NestedDefaultRouter(router,"cart",lookup="cart")
cart_items_router.register("items",views.CartItemViewSet,basename="cart-items")

urlpatterns = router.urls + cart_items_router.urls