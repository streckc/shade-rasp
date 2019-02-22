
from .config import get_config_value

from .running import run_os_command

_sensor_command = None


def avahi_browse_sensor(config):
    command = _compute_sensor_command()
    timeout = config.get('timeout', get_config_value('timeout', 600))

    results = run_os_command(command, timeout)

    data = _parse_avahi_browse_output(results['output'])

    return {
        'type': 'net',
        'data': data,
        'error': results['error'],
        'exception': results['exception']
    }


def _compute_sensor_command(config={}, no_cache=False):
    global _sensor_command

    command = _sensor_command

    if command is None or no_cache:
        command = [
            'avahi-browse',
            '--all',
            '--parsable',
            '--terminate',
            '--verbose',
            '--resolve'
        ]

        _sensor_command = command

    return command


def _parse_avahi_browse_output(output):
    prep = {}
    data = []

    if not output:
        return data

    lines = output.strip().split('\n')

    for line in lines:
        fields = line.split(';')
        if len(fields) > 0 and fields[0] == '=':
            ip_addr = fields[7]

            if ip_addr not in prep:
                prep[ip_addr] = []

            prep[ip_addr].append({
                'proto': fields[2],
                'label': _decode_labels(fields[3]),
                'service': fields[4],
                'domain': fields[5],
                'sd_addr': fields[6],
                'port': fields[8],
                'extra': fields[9]
            })

    for ip_addr in prep:
        data.append({
            'ip_addr': ip_addr,
            'discovery': prep[ip_addr]
        })

    return data


def _decode_labels(target):
    parts = target.split('\\')
    result = parts[0]

    for part in parts[1:]:
        result += chr(int(part[:3]))
        result += part[3:]

    return result

