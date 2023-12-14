from rest_framework import serializers
from cloths.models import Cloth
from accounts.models import Profile

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloth
        fields = ['id',
                  'title',
                  'author',
                  'description',
                  'price',
                  'active',
                  'season',
                  'gender',
                  'datetime_created',
                  'datetime_modified',]
        
        read_only_fields = ['author']
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = Profile.objects.get(user_id=request.user.id)
        return super().create(validated_data)