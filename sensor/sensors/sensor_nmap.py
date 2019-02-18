
import socket

import xml.etree.ElementTree as ET

from .config import get_config_value

from .running import run_os_command

_sensor_command = None

_port_props = ('name', 'product', 'version', 'tunnel', 'ostype', 'extrainfo')

def nmap_sensor(config):
    command = _compute_sensor_command()
    timeout = config.get('timeout', get_config_value('timeout', 600))

    results = run_os_command(command, timeout)

    data = _parse_nmap_output(results['output'])

    return {
        'type': 'net',
        'data': data,
        'error': results['error'],
        'except': results['except']
    }


def _compute_sensor_command(config={}, no_cache=False):
    global _sensor_command

    command = None

    #nmap -T4 -A -v -oG - 192.168.1.0/24
    if _sensor_command is None or no_cache:
        command = ['nmap', '-oX', '-']

        if config.get('level', 'basic') == 'all':
            command.extend(['-T4', '-A'])
        else:
            command.extend(['-sS'])

        ip_addr = config.get('ip_addr', _get_ip_address())
        mask = config.get('mask', '24')

        command.append('{}/{}'.format(ip_addr, mask))

        _sensor_command = command
    else:
        command = _sensor_command

    return command


def _parse_nmap_output(output):
    global _port_props
    data = []

    if not output:
        return data

    root = ET.fromstring(output)

    for host in root.findall('./host/status[@state="up"]/..'):
        ip_addr = host.find('address').attrib['addr']
        item = {
            'ip_addr': ip_addr,
            'hostnames': [],
            'ports': []
        }


        for hostname in host.findall('.hostnames/hostname'):
            if 'name' in hostname.attrib:
                data.append({
                    'ip_addr': ip_addr,
                    'hostname': hostname.attrib['name']
                })

        for port in host.findall('.ports/port'):
            port_id = '{}/{}'.format(port.attrib['protocol'], port.attrib['portid'])
            port_item = {
                'port_id': port_id
            }

            service = port.find('service').attrib
            for prop in _port_props:
                if prop in service:
                    port_item[prop] = service[prop]
                #else:
                #    port_item[prop] = None

            data.append({
                'ip_addr': ip_addr,
                'port': port_item
            })

    return data


def _get_ip_address():
    ip_addr = None
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

