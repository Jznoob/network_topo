from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Device, Interface, Link, Vlan, HistorySnapshot

# Create your views here.
def net_topology_api(request):
    devices = Device.objects.all()
    nodes = []
    device_id_map = {} # 记录设备的id映射（方便前端使用）

    for device in devices:
        node = {
            "id" : device.id,
            "name" : device.name,
            "ip" : device.ip,
            "mac" : device.mac,
            "vendor" : device.vendor,
            "status" : device.status,
        }
        nodes.append(node)
        device_id_map[device.id] = device.name

    links = []
    for link in Link.objects.select_related("interface_a", "interface_b"):
        sourcenode = device_id_map[link.interface_a.device.id]
        targetnode = device_id_map[link.interface_b.device.id]
        link_data = {
            "source" : sourcenode,
            "target" : targetnode,
            "status" : link.status,
            "link_type" : link.link_type,
            "status" : link.status,
        }
        links.append(link_data)
    return JsonResponse({
        "nodes" : nodes,
        "links" : links,
    }, safe=False)
