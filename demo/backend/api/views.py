import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt
def login_api(request):
    if request.method != 'POST':
        return JsonResponse({'code': 405, 'msg': '只允许 POST 请求'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except Exception:
        return JsonResponse({'code': 400, 'msg': '请求体格式错误'}, status=400)

    if not username or not password:
        return JsonResponse({'code': 400, 'msg': '用户名和密码不能为空'}, status=400)

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return JsonResponse({'code': 200, 'msg': '登录成功'})
    else:
        return JsonResponse({'code': 401, 'msg': '用户名或密码错误'}, status=401)
