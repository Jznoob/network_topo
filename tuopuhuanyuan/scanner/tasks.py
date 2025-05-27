# scanner/tasks.py

from celery import shared_task
from .models import ScanTask
from .scanner_service import ScannerService

@shared_task
def run_scan_task(task_id):
    task = ScanTask.objects.get(id=task_id)
    scanner = ScannerService()
    scanner.start_scan(task)
