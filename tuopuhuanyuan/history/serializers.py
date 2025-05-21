from rest_framework import serializers
from .models import History

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('id', 'action', 'description', 'data', 'created_at')
        read_only_fields = ('id', 'created_at') 