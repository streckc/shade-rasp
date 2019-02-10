
import json

from .config import set_config

from .sensor_arp_scan import _compute_sensor_command
from .sensor_arp_scan import _parse_arp_scan_output


def test_compute_sensor_command():
    base_command = ['sudo', 'arp-scan', '--retry=8', '--ignoredups', '--localnet']

    assert _compute_sensor_command() == base_command

    set_config({ 'environment': { 'interface': 'wlan0' } })
    assert _compute_sensor_command({}, True) == base_command + ['-I', 'wlan0']

    set_config({ 'environment': { 'root': '/tmp' } })
    expect = base_command + ['--macfile=/tmp/etc/mac-vendor.txt']
    assert _compute_sensor_command({}, True) == expect

    set_config({ 'environment': { 'interface': 'wlan0', 'root': '/tmp' } })
    expect = base_command + ['-I', 'wlan0', '--macfile=/tmp/etc/mac-vendor.txt']
    assert _compute_sensor_command({}, True) == expect


def test_parse_arp_scan_output():
    output = ''
    with open('test_arp_scan.txt', 'r') as fin:
        output = fin.read()

    expect = []
    with open('test_arp_scan.json', 'r') as fin:
        expect = json.load(fin)

    assert _parse_arp_scan_output(None) == []
    assert _parse_arp_scan_output('') == []
    assert _parse_arp_scan_output(output) == expect

