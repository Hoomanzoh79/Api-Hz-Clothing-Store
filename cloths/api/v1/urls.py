from . import views
from rest_framework.routers import DefaultRouter
from django.urls import path

app_name = "api-v1"

router = DefaultRouter()
router.register("cloth", views.ClothModelViewSet, basename="cloth")

urlpatterns = router.urls

urlpatterns += [
    path(
        "comment_list/cloth/<int:cloth_id>/",
        views.CommentListCreateView.as_view(),
        name="comment_list",
    ),
    path(
        "comment_detail/cloth/<int:cloth_id>/comment/<int:comment_id>/",
        views.CommentDetailView.as_view(),
        name="comment_detail",
    ),
]
