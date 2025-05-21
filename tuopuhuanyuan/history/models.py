from django.db import models
from django.contrib.auth.models import User

class History(models.Model):
    """
    历史记录模型
    """
    ACTION_CHOICES = (
        ('create', '创建'),
        ('update', '更新'),
        ('delete', '删除'),
        ('analyze', '分析'),
        ('export', '导出'),
        ('import', '导入'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='histories', verbose_name='用户')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name='操作类型')
    description = models.CharField(max_length=200, verbose_name='操作描述')
    data = models.JSONField(verbose_name='操作数据')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(verbose_name='用户代理')

    class Meta:
        verbose_name = '历史记录'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.created_at}"

class HistoryDetail(models.Model):
    """
    历史记录详情模型
    """
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name='details', verbose_name='历史记录')
    field_name = models.CharField(max_length=50, verbose_name='字段名')
    old_value = models.TextField(blank=True, null=True, verbose_name='旧值')
    new_value = models.TextField(blank=True, null=True, verbose_name='新值')

    class Meta:
        verbose_name = '历史记录详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.history} - {self.field_name}"
