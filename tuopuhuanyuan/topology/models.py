from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Device(models.Model):
    """
    设备模型
    """
    name = models.CharField(max_length=100, verbose_name='设备名称')
    ip = models.CharField(max_length=100, verbose_name='IP地址')
    mac = models.CharField(max_length=100, verbose_name='MAC地址')
    vendor = models.CharField(max_length=100, verbose_name='厂商')
    os_version = models.CharField(max_length=100, verbose_name='操作系统版本')
    location = models.CharField(max_length=100, verbose_name='位置')
    status = models.CharField(max_length=100, verbose_name='状态')
    last_seen = models.DateTimeField(auto_now=True, verbose_name='最后发现时间')
    def __str__(self):
        return f"{self.name} - {self.ip}"
    
class Interface(models.Model):
    """
    接口模型
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='interfaces', verbose_name='设备')
    name = models.CharField(max_length=100, verbose_name='接口名称')
    ip = models.CharField(max_length=100, verbose_name='IP地址')
    mac = models.CharField(max_length=100, verbose_name='MAC地址')
    status = models.CharField(max_length=100, verbose_name='状态')
    def __str__(self):
        return f"{self.device.name} - {self.name}"

class Link(models.Model):
    """
    链路模型
    """
    interface_a = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name='link_a', verbose_name='接口A')
    interface_b = models.ForeignKey(Interface, on_delete=models.CASCADE, related_name='link_b', verbose_name='接口B')
    status = models.CharField(max_length=100, verbose_name='状态')
    link_type = models.CharField(max_length=100, verbose_name='链路类型')
    def __str__(self):
        return f"{self.interface_a.device.name} - {self.interface_a.name} - {self.interface_b.name}"
    
class Vlan(models.Model):
    """
    VLAN模型
    """
    name = models.CharField(max_length=100, verbose_name='VLAN名称')
    number = models.IntegerField(verbose_name='VLAN号')
    def __str__(self):
        return f"{self.name} - {self.number}"

class HistorySnapshot(models.Model):
    """
    历史快照模型
    """
    created_at = models.DateTimeField(auto_now_add=True)
    snapshot_json = models.JSONField()

    
