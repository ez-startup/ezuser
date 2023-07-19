import socket
from django.shortcuts import render
import requests
from .utils import get_geoip_data
import uuid

def GeoIPView(request):
    # Get the client's IP address
    computer_name = socket.gethostname() 
    response = requests.get('https://api.ipify.org?format=json')
    data = response.json()        
    client_ip = socket.gethostbyname(socket.gethostname())
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])

    
    
    # Use socket to get the IP address if REMOTE_ADDR is not available
    if not client_ip:
        try:
            client_ip = data['ip']
            # return client_ip
        
        except requests.RequestException:
            client_ip = request.META.get('REMOTE_ADDR')
        
        

    # Rest of the code to retrieve geolocation data and render the template
    city_data = get_geoip_data(client_ip, 'GeoIP2-City.mmdb')
    country_data = get_geoip_data(client_ip, 'GeoIP2-Country.mmdb')
    isp_data = get_geoip_data(client_ip, 'GeoIP2-ASN.mmdb')

    return render(request, 'user/settings/ipinfo.html', {
        'city_data': city_data,
        'country_data': country_data,
        'isp_data': isp_data, 
        'client_ip': client_ip,
        'computer_name': computer_name,
        'mac_address': mac_address
    })

