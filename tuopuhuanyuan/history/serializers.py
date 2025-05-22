from rest_framework import serializers
from .models import History, HistoryDetail
from django.contrib.auth.models import User

class HistoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryDetail
        fields = ['id', 'field_name', 'old_value', 'new_value']


class HistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    details = HistoryDetailSerializer(many=True, read_only=True)
    node_count = serializers.SerializerMethodField()
    class Meta:
        model = History
        fields = [
            'id',
            'description',     # 对应“名称”
            'created_at',      # 创建时间
            'node_count',      # 节点数量
        ]
    def get_node_count(self, obj):
        return obj.data.get("node_count", None)