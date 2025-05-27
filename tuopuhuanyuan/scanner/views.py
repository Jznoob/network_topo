from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import ScanTask, ScanResult
from .scanner_service import ScannerService
from .utils.pgdm import predict_ports
from django.core.exceptions import ValidationError
from .tasks import run_scan_task
# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def submit_scan_task(request):
    try:
        data = json.loads(request.body)
        target = data.get('target')
        scan_type = data.get('scan_type')
        print(target, scan_type)
        if not target or not scan_type:
            return JsonResponse({
                'error': 'Missing required fields: target and scan_type'
            }, status=400)
            
        if scan_type not in dict(ScanTask.SCAN_TYPES):
            return JsonResponse({
                'error': f'Invalid scan type. Must be one of: {", ".join(dict(ScanTask.SCAN_TYPES).keys())}'
            }, status=400)
        
        # Create scan task with basic info
        task_data = {
            'target': target,
            'scan_type': scan_type
        }
        
        # Add scan type specific configuration
        if scan_type == 'masscan':
            scan_ports = data.get('scan_ports')
            print(scan_ports)
            if isinstance(scan_ports, list):
                scan_ports = ','.join(scan_ports)
            task_data.update({
                'scan_rate': data.get('scan_rate'),
                'scan_ports': scan_ports,
                'scan_interface': data.get('scan_interface'),
                'scan_wait': data.get('scan_wait')
            })
        elif scan_type == 'snmpwalk':
            task_data.update({
                'snmp_community': data.get('snmp_community'),
                'snmp_version': data.get('snmp_version'),
                'snmp_mib': data.get('snmp_mib')
            })
        
        # Create scan task
        task = ScanTask.objects.create(**task_data)
        
        # Start scanning in background
        run_scan_task.delay(task.id)
        
        return JsonResponse({
            'task_id': task.id,
            'status': task.status,
            'message': 'Scan task submitted successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_scan_status(request, task_id):
    try:
        task = ScanTask.objects.get(id=task_id)
        results = ScanResult.objects.filter(task=task).values()
        
        response_data = {
            'task_id': task.id,
            'status': task.status,
            'target': task.target,
            'scan_type': task.scan_type,
            'created_at': task.created_at,
            'started_at': task.started_at,
            'completed_at': task.completed_at,
            'error_message': task.error_message,
            'results': list(results)
        }
        
        # Add scan type specific configuration to response
        if task.scan_type == 'masscan':
            response_data.update({
                'scan_rate': task.scan_rate,
                'scan_ports': task.scan_ports,
                'scan_interface': task.scan_interface,
                'scan_wait': task.scan_wait
            })
        elif task.scan_type == 'snmpwalk':
            response_data.update({
                'snmp_community': task.snmp_community,
                'snmp_version': task.snmp_version,
                'snmp_mib': task.snmp_mib
            })
        
        return JsonResponse(response_data)
    except ScanTask.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

# @require_http_methods(["GET"])
# def list_scan_tasks(request):
#     tasks = ScanTask.objects.all().order_by("-created_at")[:50]
#     return JsonResponse({
#         "tasks": list(tasks.values("id", "target", "status", "scan_type", "started_at", "completed_at"))
#     })
