from django.db import models
from django.contrib.auth.models import User

class Topology(models.Model):
    """
    拓扑图模型
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topologies', verbose_name='用户')
    name = models.CharField(max_length=100, verbose_name='拓扑名称')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    data = models.JSONField(verbose_name='拓扑数据')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    tags = models.CharField(max_length=200, blank=True, null=True, verbose_name='标签')

    class Meta:
        verbose_name = '拓扑图'
        verbose_name_plural = verbose_name
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class TopologyAnalysis(models.Model):
    """
    拓扑分析结果模型
    """
    topology = models.ForeignKey(Topology, on_delete=models.CASCADE, related_name='analyses', verbose_name='拓扑图')
    analysis_type = models.CharField(max_length=50, verbose_name='分析类型')
    result = models.JSONField(verbose_name='分析结果')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    status = models.CharField(max_length=20, default='completed', verbose_name='状态')

    class Meta:
        verbose_name = '拓扑分析'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.topology.name} - {self.analysis_type} 分析"
