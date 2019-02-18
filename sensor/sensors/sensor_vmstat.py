
from .config import get_config_value

from .running import run_os_command


def vmstat_sensor(config):
    command = _compute_sensor_command()
    timeout = config.get('timeout', get_config_value('timeout', 600))

    results = run_os_command(command, timeout)

    data = _parse_vmstat_output(results['output'])

    return {
        'type': 'sys',
        'data': data,
        'error': results['error'],
        'except': results['except']
    }


def _compute_sensor_command(config={}, no_cache=False):
    return ['vmstat', '1', '2']


def _parse_vmstat_output(output):
    data = []

    if not output:
        return data

    lines = output.strip().split('\n')

    fields = [int(v) for v in lines[-1].split()]
    #procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
    # r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st

    data.append({
       'procs_run': fields[0],
       'procs_sleep': fields[1],
       'mem_swpd': fields[2],
       'mem_free': fields[3],
       'mem_buff': fields[4],
       'mem_cache': fields[5],
       'cpu_user': fields[12],
       'cpu_sys': fields[13],
       'cpu_idle': fields[14],
       'cpu_wait': fields[15]
    })

    return data

