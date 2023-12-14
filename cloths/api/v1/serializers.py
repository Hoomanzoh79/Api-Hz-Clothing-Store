from rest_framework import serializers
from cloths.models import Cloth
from accounts.models import Profile

class ClothSerializer(serializers.ModelSerializer):
    # relative_path = serializers.URLField(source='api_get_absolute_url',read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_absolute_url',)
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
                  'absolute_url',
                  'datetime_created',
                  'datetime_modified',]
        
        read_only_fields = ['author']
    
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author"] = Profile.objects.get(user_id=request.user.id)
        return super().create(validated_data)
    
    def get_absolute_url(self,obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)