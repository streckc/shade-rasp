
from .util import now
from time import time

def report_sensor_run(config):
    start = report_time()

    ret = {}

    if 'run' in config:
        ret = config['run'](config)

    end = report_time()

    return {
        'name': config.get('name', 'unknown_sensor'),
        'start': start,
        'end': end,
        'data': ret.get('data', []),
        'error': ret.get('error', None),
        'except': ret.get('except', None)
    }


def report_time():
    return time()
