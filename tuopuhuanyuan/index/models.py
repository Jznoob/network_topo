from django.db import models
from django.contrib.auth.models import User

class SystemLog(models.Model):
    """
    系统日志模型
    """
    LOG_LEVEL_CHOICES = (
        ('info', '信息'),
        ('warning', '警告'),
        ('error', '错误'),
        ('debug', '调试'),
    )

    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES, verbose_name='日志级别')
    message = models.TextField(verbose_name='日志信息')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='system_logs', verbose_name='用户')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    module = models.CharField(max_length=50, verbose_name='模块')
    action = models.CharField(max_length=50, verbose_name='操作')

    class Meta:
        verbose_name = '系统日志'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_level_display()} - {self.module} - {self.created_at}"

class Notification(models.Model):
    """
    通知模型
    """
    NOTIFICATION_TYPE_CHOICES = (
        ('system', '系统通知'),
        ('alert', '告警通知'),
        ('update', '更新通知'),
        ('other', '其他通知'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='用户')
    title = models.CharField(max_length=200, verbose_name='通知标题')
    content = models.TextField(verbose_name='通知内容')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name='通知类型')
    is_read = models.BooleanField(default=False, verbose_name='是否已读')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='阅读时间')

    class Meta:
        verbose_name = '通知'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class DashboardWidget(models.Model):
    """
    仪表盘组件模型
    """
    WIDGET_TYPE_CHOICES = (
        ('chart', '图表'),
        ('stat', '统计'),
        ('list', '列表'),
        ('custom', '自定义'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_widgets', verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='组件名称')
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPE_CHOICES, verbose_name='组件类型')
    config = models.JSONField(verbose_name='组件配置')
    position = models.IntegerField(verbose_name='位置')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '仪表盘组件'
        verbose_name_plural = verbose_name
        ordering = ['position']

    def __str__(self):
        return f"{self.name} - {self.get_widget_type_display()}"
