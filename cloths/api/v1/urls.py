from . import views
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()
router.register("cloth", views.ClothModelViewSet, basename="cloth")

urlpatterns = router.urls