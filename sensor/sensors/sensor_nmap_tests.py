
import json

from .sensor_nmap import _compute_sensor_command
from .sensor_nmap import _get_ip_address
from .sensor_nmap import _parse_nmap_output


def test_get_ip_address():
    print('Will fail on not 192.168 network')
    assert _get_ip_address()[:7] == '192.168'


def test_compute_sensor_command():
    command = ['sudo', 'nmap', '-T4', '-A', '-v', '-oX', '-']

    ip_addr = _get_ip_address()
    assert _compute_sensor_command() == command + ['{}/24'.format(ip_addr)]

    config = { 'ip_addr': '192.168.1.100' }
    assert _compute_sensor_command(config, True) == command + ['192.168.1.100/24']

    config = { 'ip_addr': '192.168.1.100', 'mask': '26' }
    assert _compute_sensor_command(config, True) == command + ['192.168.1.100/26']

    config = { 'ip_addr': '8.8.8.8', 'mask': '8' }
    assert _compute_sensor_command(config) == command + ['192.168.1.100/26']


def test_parse_nmap_output():
    output = ''
    with open('test_nmap.xml', 'r') as fin:
        output = fin.read()

    expect = []
    with open('test_nmap.json', 'r') as fin:
        expect = json.load(fin)

    assert _parse_nmap_output(None) == []
    assert _parse_nmap_output('') == []
    assert _parse_nmap_output(output) == expect

