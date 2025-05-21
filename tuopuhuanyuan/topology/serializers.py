from rest_framework import serializers
from .models import Topology

class TopologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Topology
        fields = ('id', 'name', 'description', 'data', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at') 