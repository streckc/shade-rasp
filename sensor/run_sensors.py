#!/usr/bin/env python3

import argparse
import json
import signal
import sys

from os import path

from time import time
from time import sleep

from sensors.config import get_config
from sensors.config import set_config
from sensors.config import update_config
from sensors.config import get_config_value

from sensors.reporting import report_sensor_run

from sensors.storage import init_cache
from sensors.storage import clear_cache
from sensors.storage import close_cache
from sensors.storage import store_data
from sensors.storage import send_data

from sensors.util import display
from sensors.util import log_message
from sensors.util import make_list
from sensors.util import now
from sensors.util import today
from sensors.util import set_display_timestamp
from sensors.util import set_display_verbose

from sensors import sensor_list

_log_key = path.basename(__file__)
_log_file_template = False
set_config({
    'api': { 'port': 8088 },
    'delay': 60,
    'environment': {
        'root': path.dirname(path.dirname(__file__))
    }
})

def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)


def output(message, key=None):
    global _log_key, _log_file_template

    if key is None:
        key = _log_key

    display(message)

    if _log_file_template is not False:
        filename = _log_file_template.replace('__DATE__', today())
        log_message(message, key, filename)


def read_config(filename):
    loaded = {}

    if path.isfile(filename):
        with open(filename, 'r') as fin:
            loaded = json.loads(fin.read())

    update_config(loaded)


def sort_by_priority(elem):
    return elem.get('priority', 999)


def get_active_sensors(sensors):
    run_list = []

    for key in sensors:
        if key in sensor_list:
            sensor = sensors[key]
            sensor['active'] = sensor.get('active', False)
            sensor['name'] = key

            if 'priority' not in sensor:
                sensor['priority'] = 999

            if sensors[key].get('active', False):
                output('Sensor activated: {}'.format(json.dumps(sensor, sort_keys=True)))
                sensor['run'] = sensor_list[key]
                run_list.append(sensor)
            else:
                output('Sensor not activated: {}'.format(json.dumps(sensor, sort_keys=True)))
        else:
            output('ERROR: Sensor not found: {}'.format(key))

    return sorted(run_list, key=sort_by_priority)


def run_sensors(sensors):
    data = {}

    for sensor in sensors:
        data = report_sensor_run(sensor)
        
        if data['data']:
            store_data(data)
        elif data['error']:
            output('ERROR: {}'.format(data['error']), sensor['name'])

        output('Run {:.3f}s'.format(data['end'] - data['start']), sensor['name'])

    return data


# Command line

def parse_args(sys_args):
    global _log_key, _log_file_template

    parser = argparse.ArgumentParser(description='Sensor Runner')

    parser.add_argument('-t', '--timestamp', action='store_true',
                        help='add timestamp to all output')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='additional output where available')

    parser.add_argument('-c', '--config', nargs=1, type=str, default='etc/config.json',
                        help='config file location')
    parser.add_argument('-d', '--delay', nargs=1, type=int, default=-1,
                        help='delay between sensor polls')
    parser.add_argument('-l', '--log', nargs=1, default=False,
                        help='output to log file with format')


    args = parser.parse_args(sys_args)

    set_display_timestamp(args.timestamp)
    set_display_verbose(args.verbose)

    if args.log is not False and len(args.log) > 0:
        _log_file_template = args.log[0]

    read_config(make_list(args.config)[0])

    return args


def main(sys_args):
    args = parse_args(sys_args)

    output('Starting {}'.format(json.dumps(get_config())))

    delay = int(get_config_value('delay'))

    init_cache(get_config_value('storage', 'var/cache'))

    run_list = get_active_sensors(get_config_value('sensors', []))

    if len(run_list) > 0:
        try:
            while True:
                run_sensors(run_list)
                send_data()
                sleep(delay)
        finally:
            close_cache()
            output('Shutdown')
    else:
        output('No sensors found to run.')


if __name__ == "__main__":
    main(sys.argv[1:])
