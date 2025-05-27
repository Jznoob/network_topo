from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class ScanTask(models.Model):
    SCAN_TYPES = [
        ('nmap', 'Nmap Scan'),
        ('masscan', 'Masscan Scan'),
        ('snmpwalk', 'SNMP Walk'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]   
    ip_range = models.CharField(max_length=100)
    asn = models.CharField(max_length=20, null=True, blank=True)
    geo = models.CharField(max_length=10, null=True, blank=True)
    
    target = models.CharField(max_length=255, help_text="Target IP or IP range (e.g., 192.168.1.0/24)")
    scan_type = models.CharField(max_length=20, choices=SCAN_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    
    # Masscan specific configuration
    scan_rate = models.CharField(max_length=20, null=True, blank=True, 
                               help_text="Packets per second for masscan")
    scan_ports = models.CharField(max_length=100, null=True, blank=True,
                                help_text="Port range for masscan (e.g., 1-65535)")
    scan_interface = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="Network interface for masscan")
    scan_wait = models.CharField(max_length=20, null=True, blank=True,
                               help_text="Wait time for masscan")
    
    # SNMP specific configuration
    snmp_community = models.CharField(max_length=100, null=True, blank=True,
                                    help_text="SNMP community string")
    snmp_version = models.CharField(max_length=10, null=True, blank=True,
                                  help_text="SNMP version (1, 2c, 3)")
    snmp_mib = models.CharField(max_length=255, null=True, blank=True,
                              help_text="SNMP MIB to query")
    
    def __str__(self):
        return f"{self.scan_type} scan of {self.target}"

    def validate_scan_config(self):
        if self.scan_type == 'masscan':
            if self.scan_rate and int(self.scan_rate) > 10000:
                raise ValidationError('Scan rate too high')

class ScanResult(models.Model):
    task = models.ForeignKey(ScanTask, on_delete=models.CASCADE, related_name='results')
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField(null=True, blank=True)
    protocol = models.CharField(max_length=10, null=True, blank=True)
    service = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=100, null=True, blank=True)
    os_info = models.CharField(max_length=255, null=True, blank=True)
    snmp_data = models.JSONField(null=True, blank=True)
    raw_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']  # 默认按照创建时间倒序排列
        db_table = 'scan_results'  # 使用自定义表名
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['task']),
        ]
    
    def __str__(self):
        return f"Result for {self.ip_address} from {self.task}"

