
from .config import get_config_value

from .running import run_os_command

_sensor_command = None


def arp_scan_sensor(config):
    command = _compute_sensor_command()
    timeout = config.get('timeout', get_config_value('timeout', 600))

    results = run_os_command(command, timeout)

    data = _parse_arp_scan_output(results['output'])

    return {
        'data': data,
        'error': results['error'],
        'except': results['except']
    }


def _compute_sensor_command(config={}, no_cache=False):
    global _sensor_command

    command = _sensor_command

    if command is None or no_cache:
        command = [
            'arp-scan',
            '--retry=8',
            '--ignoredups',
            '--localnet'
        ]

        interface = get_config_value('environment.interface')
        if interface:
            command.extend(['-I', interface])

        root = get_config_value('environment.root')
        if root:
            command.append('--macfile={}/etc/mac-vendor.txt'.format(root))

        _sensor_command = command

    return command


def _parse_arp_scan_output(output):
    data = []

    if not output:
        return data

    lines = output.strip().split('\n')

    for line in lines:
        if '\t' in line:
            fields = line.split('\t')
            data.append({
                'ip_addr': fields[0],
                'mac_addr': fields[1],
                'mac_manu': fields[2]
            })

    return data

