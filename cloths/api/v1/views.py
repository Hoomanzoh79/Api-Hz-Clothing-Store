from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from cloths.models import Cloth
from .serializers import ClothSerializer
from .paginations import DefaultPagination
from .permissions import IsOwnerOrReadOnly


class ClothModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClothSerializer
    queryset = Cloth.objects.filter(active=True)
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    pagination_class = DefaultPagination