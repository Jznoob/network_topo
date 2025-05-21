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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """
    用户注册 API
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        # 创建用户
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],  # 注意：实际应用中应该加密密码
            email=serializer.validated_data['email']
        )
        # 创建用户档案
        UserProfile.objects.create(user=user)
        return Response({
            'message': '注册成功',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
    try:
        profile = UserProfile.objects.get(user=request.user)
        return Response({
            'user': UserSerializer(request.user).data,
            'profile': {    
                'phone': profile.phone,
                'avatar': profile.avatar.url if profile.avatar else None,
                'bio': profile.bio,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at
            }
        })
    except UserProfile.DoesNotExist:
        return Response({'error': '用户档案不存在'}, status=status.HTTP_404_NOT_FOUND)

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
        'Reset Password Verification Code',
        f'Your verification code is: {code}, valid within 10 minutes.',
        [email],
        fail_silently=False,
    )
    
    return Response({
        'message': 'Reset password email has been sent',
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_api(request):
    email = request.data.get('email')
    code = request.data.get('code')
    new_password = request.data.get('new_password')

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
