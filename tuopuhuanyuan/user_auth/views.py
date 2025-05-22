import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from .models import User, UserProfile,  LoginHistory, EmailVerificationCode
from django.utils import timezone
import uuid
from datetime import timedelta
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .serializers import EmailSerializer
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def register_api_1(request):
    print("bug")
    serializer = EmailSerializer(data=request.data)
    print("bug11")
    if serializer.is_valid():
        email = serializer.validated_data['email']

        # 生成6位数字验证码
        verification_code = str(random.randint(100000, 999999))
        
        # 缓存验证码，设置过期时间，比如10分钟
        cache_key = f'register_code_{email}'
        cache.set(cache_key, {
            'code': verification_code,
        }, timeout=600)  # 600秒=10分钟

        # 发送邮件
        send_mail(
            subject='注册验证码',
            message=f'您的验证码是 {verification_code}，有效期10分钟。',
            from_email=None,  # 默认发件人
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({'message': '验证码已发送，请检查邮箱'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
@csrf_exempt
def register_api(request):
    email = request.data.get('email')
    code = request.data.get('code')
    username = request.data.get('username')
    password = request.data.get('password')
    if not email or not code:
        return Response({'error': '邮箱和验证码不能为空'}, status=status.HTTP_400_BAD_REQUEST)

    cache_key = f'register_code_{email}'
    cached = cache.get(cache_key)
    print(f"[DEBUG] cache key: register_code_{email}")
    print(f"[DEBUG] cached data: {cache.get(cache_key)}")
    if cached is None:
        return Response({'error': '验证码已过期或不存在'}, status=status.HTTP_400_BAD_REQUEST)
    if cached['code'] != code:
        print(f'{cached["code"]}')
        return Response({'error': '验证码错误'}, status=status.HTTP_400_BAD_REQUEST)

    # 验证码正确，创建用户
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
    )
    UserProfile.objects.create(user=user)

    # 验证完成后清理缓存
    cache.delete(cache_key)

    return Response({'message': '注册成功'}, status=status.HTTP_201_CREATED)
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("POST data:", data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

        username = data.get('username')
        password = data.get('password')

        print("username:", username)
        print("password:", password and "存在")

        if not username or not password:
            return JsonResponse({'status': 'error', 'message': '用户名和密码不能为空'}, status=400)

        try:
            user = User.objects.get(username=username)
            print("找到用户:", user.username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['username'] = user.username

                return JsonResponse({
                    'status': 'success',
                    'message': '登录成功',
                    'user': UserSerializer(user).data
                })
            else:
                return JsonResponse({'status': 'error', 'message': '密码错误'}, status=400)
        except User.DoesNotExist:
            print("用户不存在:", username)
            return JsonResponse({'status': 'error', 'message': '用户不存在'}, status=400)

    elif request.method == 'GET':
        return JsonResponse({'csrf_token': get_token(request)})

    return JsonResponse({'status': 'error', 'message': '不支持的请求方法'}, status=405)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': '登出成功'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    """
    获取用户信息 API
    """
    print(f"用户: {request.user}, 认证状态: {request.user.is_authenticated}")
    return Response({
        'user': UserSerializer(request.user).data,
        'profile': {
            'username' : request.user.username,
            'email' : request.user.email,
            'created_at' : request.user.date_joined,
        }
    })
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_api(request):
    """
    更新用户信息 API
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
        # 更新用户基本信息
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        
        # 更新用户档案
        profile_data = request.data.get('profile', {})
        if profile_data:
            profile.phone = profile_data.get('phone', profile.phone)
            profile.bio = profile_data.get('bio', profile.bio)
            if 'avatar' in profile_data:
                profile.avatar = profile_data['avatar']
            profile.save()
        
        return Response({
            'message': '更新成功',
            'user': UserSerializer(request.user).data,
            'profile': {
                'phone': profile.phone,
                'avatar': profile.avatar.url if profile.avatar else None,
                'bio': profile.bio,
                'updated_at': profile.updated_at
            }
        })
    except UserProfile.DoesNotExist:
        return Response({'error': '用户档案不存在'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_api(request):   
    """
    忘记密码 API
    """
    email = request.data.get('email')
    if not email:
        return Response({'error': '请提供邮箱地址'}, status=status.HTTP_400_BAD_REQUEST)
    
    code = f"{random.randint(100000, 999999)}"    # 发送邮件
    EmailVerificationCode.objects.create(email=email, code=code)
    send_mail(
        'Network Topology Restoration',
        f'Reset Password Verification Code:Your verification code is: {code}, valid within 10 minutes.',
        'wenhanfan11@gmail.com',
        [email],
        fail_silently=False,
    )
    
    return Response({
        'message': 'Reset password email has been sent',
    })

@api_view(['POST'])
@permission_classes([AllowAny])

#{
#    "email" : "1113843656@qq.com",
#    "code" : "396452", 
#    "new_password" : "123321"
#}
def reset_password_api(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')
    if not email:
        print(email)
    
    if not code:
        print(code)
    if not new_password:
        print(new_password)
        
    if not email or not code or not new_password:
        return Response({'error': '缺少必要字段'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        record = EmailVerificationCode.objects.filter(email=email, code=code, is_used=False).latest('created_at')
        
        if record.is_expired():
            return Response({'error': '验证码已过期'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 获取用户
        from django.contrib.auth.models import User
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        record.is_used = True
        record.save()

        return Response({'message': '密码重置成功'})
    
    except EmailVerificationCode.DoesNotExist:
        return Response({'error': '验证码错误或已使用'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': '该邮箱未注册'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password_api(request):
    print(f"用户: {request.user}, 认证状态: {request.user.is_authenticated}")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("POST data:", data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': '无效的 JSON 数据'}, status=400)

        old_password = data.get('old_password')
        new_password = data.get('new_password')

        print("old_password:", old_password)
        print("new_password:", new_password and "存在")

        if not old_password or not new_password:
            return JsonResponse({'status': 'error', 'message': '旧密码和新密码不能为空'}, status=400)
        if len(new_password) < 8:
            return JsonResponse({'status': 'error', 'message': '新密码长度至少8位'}, status=400)

        user = request.user
        if check_password(old_password, user.password):
            user.set_password(new_password)
            user.save()
            return JsonResponse({   
               'status': 'success',
               'message': '密码修改成功',
            })
        else:
            return JsonResponse({'status': 'error', 'message': '旧密码错误'}, status=400)

    return JsonResponse({'status': 'error', 'message': '不支持的请求方法'}, status=405)
