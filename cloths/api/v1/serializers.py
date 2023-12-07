from rest_framework import serializers
from cloths.models import Cloth


class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ['id',
                  'title',
                  'description',
                  'price',
                  'active',
                  'season',
                  'gender',
                  'datetime_created',
                  'datetime_modified',]