from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from cloths.models import Cloth
from .serializers import ClothSerializer
from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


class ClothModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClothSerializer
    queryset = Cloth.objects.filter(active=True)
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_fields = {
        "author": ["exact", "in"],
    }
    search_fields = ["title","description"]
    ordering_fields = ["datetime_created"]