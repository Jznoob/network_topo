from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TopologySerializer

# Create your views here.

#@login_required
def topology_view(request):
    return render(request, 'topology.html')

#@login_required
def save_topology(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 保存拓扑图逻辑
            return JsonResponse({'status': 'success', 'message': '拓扑图保存成功'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)
#@login_required
def load_topology(request):
    if request.method == 'GET':
        # 加载拓扑图逻辑
        return JsonResponse({
            'status': 'success',
            'data': {
                'nodes': [],
                'edges': []
            }
        })
    return JsonResponse({'status': 'error', 'message': '仅支持GET请求'}, status=405)

#@login_required
def analyze_topology(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 分析拓扑图逻辑
            return JsonResponse({
                'status': 'success',
                'data': {
                    'analysis': {}
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topology_list_api(request):
    """
    获取拓扑列表 API
    """
    topologies = Topology.objects.filter(user=request.user)
    serializer = TopologySerializer(topologies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def topology_create_api(request):
    """
    创建拓扑 API
    """
    serializer = TopologySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def topology_detail_api(request, pk):
    """
    获取拓扑详情 API
    """
    try:
        topology = Topology.objects.get(pk=pk, user=request.user)
    except Topology.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TopologySerializer(topology)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def topology_update_api(request, pk):
    """
    更新拓扑 API
    """
    try:
        topology = Topology.objects.get(pk=pk, user=request.user)
    except Topology.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = TopologySerializer(topology, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def topology_delete_api(request, pk):
    """
    删除拓扑 API
    """
    try:
        topology = Topology.objects.get(pk=pk, user=request.user)
    except Topology.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    topology.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def topology_analyze_api(request, pk):
    """
    分析拓扑 API
    """
    try:
        topology = Topology.objects.get(pk=pk, user=request.user)
    except Topology.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # TODO: 实现拓扑分析逻辑
    return Response({
        'message': '拓扑分析完成',
        'analysis_result': {}  # 这里返回分析结果
    })
