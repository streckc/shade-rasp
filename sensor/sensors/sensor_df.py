
from .config import get_config_value

from .running import run_os_command


def df_sensor(config):
    command = _compute_sensor_command()
    timeout = config.get('timeout', get_config_value('timeout', 600))

    results = run_os_command(command, timeout)

    data = _parse_df_output(results['output'])

    return {
        'type': 'sys',
        'data': data,
        'error': results['error'],
        'except': results['except']
    }


def _compute_sensor_command(config={}, no_cache=False):
    return ['df', '-k']


def _parse_df_output(output):
    data = []

    if not output:
        return data

    lines = output.strip().split('\n')

    for line in lines[1:]:
        #Filesystem     1K-blocks    Used Available Use% Mounted on
        fields = line.split()
        if fields[0][0] == '/':
            data.append({
                'filesystem': fields[0],
                'mounted': fields[5],
                'kb': int(fields[1]),
                'used': int(fields[2]),
                'avail': int(fields[3])
            })

    return data

