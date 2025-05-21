from rest_framework import serializers
from .models import Config

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = ('id', 'name', 'description', 'data', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at') 