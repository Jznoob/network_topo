from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import History, HistoryDetail
from .serializers import HistorySerializer, HistoryDetailSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
# Create your views here.

@login_required
def history_view(request):
    return render(request, 'history.html')

@login_required
def get_history_list(request):
    if request.method == 'GET':
        # 获取历史记录列表逻辑
        return JsonResponse({
            'status': 'success',
            'data': {
                'records': [],
                'total': 0
            }
        })
    return JsonResponse({'status': 'error', 'message': '仅支持GET请求'}, status=405)

@login_required
def history_detail(request, history_id):
    if request.method == 'GET':
        # 获取历史记录详情逻辑
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': history_id,
                'details': {}
            }
        })
    return JsonResponse({'status': 'error', 'message': '仅支持GET请求'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_list_api(request):
    """
    获取历史记录列表 API
    """
    histories = History.objects.filter(user=request.user).order_by('-created_at')
    serializer = HistorySerializer(histories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def history_detail_api(request, pk):
    """
    获取历史记录详情 API
    """
    try:
        history = History.objects.get(pk=pk, user=request.user)
    except History.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = HistorySerializer(history)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def history_delete_api(request, pk):
    """
    删除历史记录 API
    """
    try:
        history = History.objects.get(pk=pk, user=request.user)
    except History.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    history.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def history_clear_api(request):
    """
    清空历史记录 API
    """
    History.objects.filter(user=request.user).delete()
    return Response({'message': '历史记录已清空'})

class CreateHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        history = History.objects.create(
            user=user,
            description=data.get('description', ''),
            action=data.get('action', ''),
            data=data.get('data', {}),
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
        )
        return Response({"id": history.id, "message": "历史记录创建成功"}) 

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    查看操作历史（拓扑记录使用记录）
    """
    queryset = History.objects.select_related('user').prefetch_related('details').all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['action', 'user__username']
    search_fields = ['description', 'data']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

