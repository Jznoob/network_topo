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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from .models import User, UserProfile, PasswordResetToken, LoginHistory
from django.utils import timezone
import uuid
from datetime import timedelta
from django.middleware.csrf import get_token
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


@api_view(['POST'])
@permission_classes([AllowAny])
def register_api(request):
    """
    用户注册 API
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        # 创建用户
        user = User.objects.create(
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_api(request):
    """
    用户登出 API
    """
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
    
    try:
        user = User.objects.get(email=email)
        # 创建密码重置令牌
        token = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(hours=24)  # 24小时后过期
        
        PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # TODO: 发送重置密码邮件
        # 这里应该实现发送邮件的逻辑，包含重置链接
        
        return Response({
            'message': '重置密码邮件已发送',
            'token': token  # 注意：实际应用中不应该返回token
        })
    except User.DoesNotExist:
        return Response({'error': '该邮箱未注册'}, status=status.HTTP_404_NOT_FOUND)
