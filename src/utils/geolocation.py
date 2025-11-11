import requests
from flask import request

def get_client_ip():
    """
    Get the client's IP address from the request.
    Handles proxy headers (X-Forwarded-For, X-Real-IP).
    """
    # Check for proxy headers first
    if request.headers.get('X-Forwarded-For'):
        # X-Forwarded-For can contain multiple IPs, get the first one
        ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        ip = request.headers.get('X-Real-IP')
    else:
        ip = request.remote_addr
    
    return ip

def get_location_from_ip(ip_address):
    """
    Get location information from IP address using ip-api.com (free service).
    
    Returns a dictionary with:
    - country: Country name
    - region: Region/state name
    - city: City name
    - latitude: Latitude coordinate
    - longitude: Longitude coordinate
    
    Returns None values if lookup fails or for local IPs.
    """
    # Handle local/private IPs
    if not ip_address or ip_address in ['127.0.0.1', 'localhost', '::1']:
        return {
            'country': 'Local',
            'region': 'Local',
            'city': 'Local',
            'latitude': None,
            'longitude': None
        }
    
    # Check if it's a private IP range
    if ip_address.startswith(('10.', '172.', '192.168.')):
        return {
            'country': 'Private Network',
            'region': 'Private Network',
            'city': 'Private Network',
            'latitude': None,
            'longitude': None
        }
    
    try:
        # Use ip-api.com free API (45 requests/minute limit)
        response = requests.get(
            f'http://ip-api.com/json/{ip_address}',
            timeout=3
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'latitude': data.get('lat'),
                    'longitude': data.get('lon')
                }
    except Exception as e:
        print(f"[WARNING] Geolocation lookup failed for {ip_address}: {e}")
    
    # Return unknown if lookup fails
    return {
        'country': 'Unknown',
        'region': 'Unknown',
        'city': 'Unknown',
        'latitude': None,
        'longitude': None
    }
