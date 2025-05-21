from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
    
class UserProfile(models.Model):
    """
    用户扩展信息模型
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, null=True, verbose_name='个人简介')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的个人信息"

class PasswordResetToken(models.Model):
    """
    密码重置令牌模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_tokens')
    token = models.CharField(max_length=100, unique=True, verbose_name='重置令牌')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expires_at = models.DateTimeField(verbose_name='过期时间')
    is_used = models.BooleanField(default=False, verbose_name='是否已使用')

    class Meta:
        verbose_name = '密码重置令牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的密码重置令牌"

    def is_valid(self):
        """
        检查令牌是否有效
        """
        return not self.is_used and self.expires_at > timezone.now()

class LoginHistory(models.Model):
    """
    登录历史记录模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_histories')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(verbose_name='用户代理')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    is_successful = models.BooleanField(default=True, verbose_name='是否成功')

    class Meta:
        verbose_name = '登录历史'
        verbose_name_plural = verbose_name
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username}的登录记录 - {self.login_time}"
    