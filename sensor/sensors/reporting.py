
from .util import now
from time import time

def report_sensor_run(config):
    start = report_time()

    ret = {}

    if 'run' in config:
        ret = config['run'](config)

    end = report_time()

    report = {
        'name': config.get('name', 'unknown_sensor'),
        'start': start,
        'end': end
    }
    report.update(ret)

    return report


def report_time():
    return time()
