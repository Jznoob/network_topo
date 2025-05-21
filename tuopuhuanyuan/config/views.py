from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Config
from .serializers import ConfigSerializer

# Create your views here.

@login_required
def config_view(request):
    return render(request, 'config.html')

@login_required
def save_config(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 保存配置逻辑
            return JsonResponse({'status': 'success', 'message': '配置保存成功'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)

@login_required
def load_config(request):
    if request.method == 'GET':
        # 加载配置逻辑
        return JsonResponse({'status': 'success', 'data': {}})
    return JsonResponse({'status': 'error', 'message': '仅支持GET请求'}, status=405)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def config_list_api(request):
    """
    获取配置列表 API
    """
    configs = Config.objects.filter(user=request.user)
    serializer = ConfigSerializer(configs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def config_create_api(request):
    """
    创建配置 API
    """
    serializer = ConfigSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def config_detail_api(request, pk):
    """
    获取配置详情 API
    """
    try:
        config = Config.objects.get(pk=pk, user=request.user)
    except Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ConfigSerializer(config)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def config_update_api(request, pk):
    """
    更新配置 API
    """
    try:
        config = Config.objects.get(pk=pk, user=request.user)
    except Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ConfigSerializer(config, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def config_delete_api(request, pk):
    """
    删除配置 API
    """
    try:
        config = Config.objects.get(pk=pk, user=request.user)
    except Config.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    config.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
