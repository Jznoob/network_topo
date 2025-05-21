from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required

#@login_required
def index(request):
    """首页视图"""
    return render(request, 'index.html')

def network(request):
    """网络配置视图"""
    return render(request, 'index/network.html')

def topology(request):
    """拓扑还原视图"""
    return render(request, 'index/topology.html')

def analysis(request):
    """网络分析视图"""
    return render(request, 'index/analysis.html')

#@csrf_exempt
def api_network_data(request):
    """网络数据API"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # 这里添加处理网络数据的逻辑
            return JsonResponse({'status': 'success', 'message': '数据接收成功'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的JSON数据'}, status=400)
    return JsonResponse({'status': 'error', 'message': '仅支持POST请求'}, status=405)
