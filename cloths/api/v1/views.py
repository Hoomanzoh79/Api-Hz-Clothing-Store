from rest_framework import viewsets
from cloths.models import Cloth
from .serializers import ClothSerializer


class ClothModelViewSet(viewsets.ModelViewSet):
    serializer_class = ClothSerializer
    queryset = Cloth.objects.filter(active=True)