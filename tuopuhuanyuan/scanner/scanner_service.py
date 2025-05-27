import subprocess
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from .models import ScanTask, ScanResult
import logging
import tempfile
import os
from celery import shared_task
from django.conf import settings
from .utils.pgdm import predict_ports

logger = logging.getLogger(__name__)

class ScannerService:
    def start_scan(self, task):
        """Start a scan task using Celery"""
        run_scan_task.delay(task.id)

@shared_task
def run_scan_task(task_id):
    """Celery task to execute the scan"""
    try:
        print(f"Starting scan task {task_id}")
        task = ScanTask.objects.get(id=task_id)
        task.status = 'running'
        task.started_at = datetime.now()
        task.save()
        
        if task.scan_type == 'nmap':
            run_nmap_scan(task)
        elif task.scan_type == 'masscan':
            run_masscan_scan(task)
        elif task.scan_type == 'snmpwalk':
            run_snmpwalk_scan(task)
        print(f"Scan task {task.id} completed")
        task.status = 'completed'
        task.completed_at = datetime.now()
        task.save()
        
    except Exception as e:
        print(f"Scan task {task_id} failed: {str(e)}")
        logger.error(f"Scan failed: {str(e)}")
        task.status = 'failed'
        task.error_message = str(e)
        task.completed_at = datetime.now()
        task.save()

def run_nmap_scan(task):
    """Execute nmap scan and parse results"""
    cmd = [
        'nmap',
        '-sS',  # TCP SYN scan
        '-sV',  # Version detection
        '-O',   # OS detection
        '-oX',  # Output in XML format
        '-',    # Output to stdout
        task.target
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        parse_nmap_xml(result.stdout, task)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Nmap scan failed: {e.stderr}")

def run_masscan_scan(task):
    print("run_masscan_scan")
    """Execute masscan scan and parse results with configurable parameters"""
    output_path = None
    try:
        logger.info(f"Starting masscan scan for task {task.id} on target {task.target}")
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as f:
            output_path = f.name
            logger.info(f"Created temporary output file: {output_path}")
        
        # 获取配置
        rate = getattr(task, 'scan_rate', getattr(settings, 'MASSCAN_DEFAULT_RATE', '1000'))
        ports = getattr(task, 'scan_ports', '22,80')
        
        logger.info(f"Using scan configuration - rate: {rate}, ports: {ports}")
        
        # 构建命令字符串
        cmd_str = f"sudo /opt/homebrew/bin/masscan {task.target} --ports {ports} --rate {rate} -oJ {output_path}"
        
        # 添加可选参数
        if hasattr(task, 'scan_interface') and task.scan_interface:
            cmd_str += f" --interface {task.scan_interface}"
        if hasattr(task, 'scan_wait') and task.scan_wait:
            cmd_str += f" --wait {task.scan_wait}"
        
        logger.info(f"Executing masscan command: {cmd_str}")
        
        # 执行命令
        try:
            process = subprocess.run(
                cmd_str,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                timeout=300  # 5分钟超时
            )
            logger.info(f"Masscan command completed with return code: {process.returncode}")
            if process.stdout:
                logger.debug(f"Masscan stdout: {process.stdout}")
            if process.stderr:
                logger.debug(f"Masscan stderr: {process.stderr}")
                
        except subprocess.TimeoutExpired:
            raise Exception("Masscan scan timed out after 5 minutes")
        except subprocess.CalledProcessError as e:
            logger.error(f"Masscan command failed with return code {e.returncode}")
            logger.error(f"Error output: {e.stderr}")
            raise Exception(f"Masscan scan failed: {e.stderr}")
        
        # 检查输出文件
        if not os.path.exists(output_path):
            raise Exception("Masscan output file was not created")
            
        # 读取结果
        try:
            with open(output_path, 'r') as f:
                json_output = f.read().strip()
                logger.info(f"Read {len(json_output)} bytes from output file")
                
            if not json_output:
                logger.warning("Masscan produced empty output")
                return
                
            # 解析结果
            parse_masscan_json(json_output, task)
            
        except Exception as e:
            logger.error(f"Error reading or parsing output file: {str(e)}")
            raise
            
    except Exception as e:
        error_msg = f"Masscan scan encountered an cmd: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)
    finally:
        # 清理临时文件
        if output_path and os.path.exists(output_path):
            try:
                os.remove(output_path)
                logger.info(f"Removed temporary file: {output_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {output_path}: {str(e)}")

def run_snmpwalk_scan(task):
    """Execute snmpwalk scan and parse results"""
    # Get SNMP configuration from task or settings
    community = getattr(task, 'snmp_community', 
                       getattr(settings, 'SNMP_DEFAULT_COMMUNITY', 'public'))
    version = getattr(task, 'snmp_version', 
                     getattr(settings, 'SNMP_DEFAULT_VERSION', '2c'))
    mib = getattr(task, 'snmp_mib', 
                  getattr(settings, 'SNMP_DEFAULT_MIB', '1.3.6.1.2.1'))
    
    cmd = [
        'snmpwalk',
        f'-v{version}',
        '-c', community,
        task.target,
        mib
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        parse_snmpwalk_output(result.stdout, task)
    except subprocess.CalledProcessError as e:
        raise Exception(f"SNMPwalk scan failed: {e.stderr}")

def parse_nmap_xml(xml_output, task):
    """Parse nmap XML output and save results with enhanced data structure"""
    try:
        root = ET.fromstring(xml_output)
        
        # 按 IP 聚合结果
        host_results = {}
        for host in root.findall('.//host'):
            ip = host.find('address').get('addr')
            if ip not in host_results:
                host_results[ip] = {
                    'ports': [],
                    'os_info': None,
                    'hostnames': []
                }
            
            # Get OS information
            os_match = host.find('.//osmatch')
            if os_match is not None:
                host_results[ip]['os_info'] = os_match.get('name')
            
            # Get hostnames
            for hostname in host.findall('.//hostname'):
                if hostname.get('name'):
                    host_results[ip]['hostnames'].append(hostname.get('name'))
            
            # Process each port
            for port in host.findall('.//port'):
                port_num = int(port.get('portid'))
                protocol = port.get('protocol')
                
                # Get port state
                state = port.find('state')
                state_info = state.attrib if state is not None else {}
                
                # Get service information
                service_elem = port.find('service')
                service_info = service_elem.attrib if service_elem is not None else {}
                
                # Extract service details
                service = service_info.get('name')
                version = service_info.get('product')
                if service_info.get('version'):
                    version = f"{version} {service_info.get('version')}" if version else service_info.get('version')
                
                # Add port to host results
                host_results[ip]['ports'].append({
                    'port': port_num,
                    'protocol': protocol,
                    'state': state_info,
                    'service': service_info
                })
                
                # Create scan result
                ScanResult.objects.create(
                    task=task,
                    ip_address=ip,
                    port=port_num,
                    protocol=protocol,
                    service=service,
                    version=version,
                    os_info=host_results[ip]['os_info'],
                    raw_data={
                        'state': state_info,
                        'service': service_info,
                        'os': host_results[ip]['os_info'],
                        'host': {
                            'ip': ip,
                            'hostnames': host_results[ip]['hostnames']
                        }
                    }
                )
        
        return host_results
        
    except ET.ParseError as e:
        raise Exception(f"Failed to parse Nmap XML output: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing Nmap results: {str(e)}")

def parse_masscan_json(json_output, task):
    """Parse masscan JSON output and save results with error handling"""
    try:
        logger.info("Starting to parse masscan JSON output")
        
        # 解析 JSON
        try:
            results = json.loads(json_output)
            logger.info(f"Successfully parsed JSON output, found {len(results) if isinstance(results, list) else 1} results")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON: {str(e)}")
            logger.error(f"JSON content: {json_output[:200]}...")  # 只记录前200个字符
            raise
        
        # 确保结果是列表
        if not isinstance(results, list):
            results = [results]
            logger.info("Converted single result to list format")
            
        # 处理每个结果
        for result in results:
            if not isinstance(result, dict):
                logger.warning(f"Skipping invalid result format: {result}")
                continue
                
            ip = result.get('ip')
            if not ip:
                logger.warning("Skipping result with no IP address")
                continue
                
            ports = result.get('ports', [])
            if not isinstance(ports, list):
                logger.warning(f"Invalid ports format for IP {ip}: {ports}")
                continue
                
            logger.info(f"Processing {len(ports)} ports for IP {ip}")
            
            # 处理每个端口
            for port_info in ports:
                if not isinstance(port_info, dict):
                    logger.warning(f"Invalid port info format for IP {ip}: {port_info}")
                    continue
                    
                try:
                    ScanResult.objects.create(
                        task=task,
                        ip_address=ip,
                        port=port_info.get('port'),
                        protocol=port_info.get('proto'),
                        raw_data={
                            'masscan_data': result,
                            'port_info': port_info
                        }
                    )
                    logger.debug(f"Created scan result for IP {ip}, port {port_info.get('port')}")
                except Exception as e:
                    logger.error(f"Failed to create scan result for IP {ip}: {str(e)}")
                    
    except Exception as e:
        error_msg = f"Error processing masscan results: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

def parse_snmpwalk_output(output, task):
    """Parse snmpwalk output and save results with enhanced data structure"""
    lines = output.strip().split('\n')
    snmp_data = {}
    
    # Extract specific SNMP fields
    sys_name = None
    sys_descr = None
    
    for line in lines:
        if '=' in line:
            oid, value = line.split('=', 1)
            oid = oid.strip()
            value = value.strip()
            snmp_data[oid] = value
            
            # Extract specific fields
            if '1.3.6.1.2.1.1.5.0' in oid:  # sysName
                sys_name = value
            elif '1.3.6.1.2.1.1.1.0' in oid:  # sysDescr
                sys_descr = value
    
    # Create a single result with all SNMP data
    ScanResult.objects.create(
        task=task,
        ip_address=task.target,
        service='SNMP',
        version=sys_descr,
        os_info=sys_name,
        snmp_data=snmp_data,
        raw_data={
            'snmp_data': snmp_data,
            'sys_name': sys_name,
            'sys_descr': sys_descr
        }
    ) 