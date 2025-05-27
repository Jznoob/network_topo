import requests
import logging

logger = logging.getLogger(__name__)

def predict_ports(ip_range, asn=None, geo=None, fallback_ports='1-65535'):
    try:
        payload = {
            "ip_range": ip_range,
            "asn": asn,
            "geo": geo
        }
        response = requests.post("http://localhost:8001/predict", json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        ports = data.get('ports')
        if not ports:
            raise ValueError("No ports returned")
        return ports
    except Exception as e:
        logger.warning(f"PGDM prediction failed: {e}, fallback to {fallback_ports}")
        return fallback_ports.split(',')