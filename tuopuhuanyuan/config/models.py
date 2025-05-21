from django.db import models
from django.contrib.auth.models import User

class Config(models.Model):
    """
    配置模型
    """
    CONFIG_TYPE_CHOICES = (
        ('system', '系统配置'),
        ('network', '网络配置'),
        ('security', '安全配置'),
        ('custom', '自定义配置'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='configs', verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='配置名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    config_type = models.CharField(max_length=20, choices=CONFIG_TYPE_CHOICES, default='custom', verbose_name='配置类型')
    data = models.JSONField(verbose_name='配置数据')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    version = models.IntegerField(default=1, verbose_name='版本号')

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']
        unique_together = ['user', 'name', 'version']

    def __str__(self):
        return f"{self.name} - {self.get_config_type_display()}"

class ConfigTemplate(models.Model):
    """
    配置模板模型
    """
    name = models.CharField(max_length=100, verbose_name='模板名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    config_type = models.CharField(max_length=20, choices=Config.CONFIG_TYPE_CHOICES, verbose_name='配置类型')
    template_data = models.JSONField(verbose_name='模板数据')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_public = models.BooleanField(default=True, verbose_name='是否公开')

    class Meta:
        verbose_name = '配置模板'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} - {self.get_config_type_display()}"
