#!/usr/bin/env python3

import argparse
import json
import signal
import sys

from copy import deepcopy

from os import path

from time import time
from time import sleep

from sensors.config import get_config
from sensors.config import set_config
from sensors.config import update_config
from sensors.config import get_config_value

from sensors.cron import start_scheduler
from sensors.cron import stop_scheduler
from sensors.cron import schedule_job
from sensors.cron import run_pending_jobs

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


def schedule_sensors(sensors):
    num_jobs = 0
    for key in sensors:
        if key in sensor_list:
            sensor = sensors[key]
            sensor['name'] = key

            if 'schedule' in sensor:
                run_sensor = deepcopy(sensor)
                run_sensor['run'] = sensor_list[key]
                result = schedule_job(
                    sensor['schedule'],
                    sensor['name'],
                    report_sensor_run,
                    run_sensor
                )
                if result:
                    num_jobs += 1
                    output('Sensor scheduled: {}'.format(json.dumps(sensor, sort_keys=True)))
                else:
                    output('ERROR: Sensor not scheduled: {}'.format(json.dumps(sensor, sort_keys=True)))
            else:
                output('Sensor not activated: {}'.format(json.dumps(sensor, sort_keys=True)))
        else:
            output('ERROR: Sensor not found: {}'.format(key))

    return num_jobs


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

    init_cache(get_config_value('storage', 'var/cache'))

    num_jobs = schedule_sensors(get_config_value('sensors', []))
    output('Jobs scheduled: {}'.format(num_jobs))

    if num_jobs > 0:
        start_scheduler()
        try:
            while True:
                data = run_pending_jobs()
                if data['jobs'] > 0:
                    output('{} jobs run in {} seconds'.format(data['jobs'], data['time']))
                    for result in data['data']:
                        output('  .. {}: {}s, {} records'.format(
                            result['name'],
                            int(result['end'] - result['start']),
                            len(result['data'])))
                        store_data(result)
    #            send_data()
                sleep(1)
        finally:
            close_cache()
            stop_scheduler()
            output('Shutdown')
    else:
        output('No sensors found to run.')


if __name__ == "__main__":
    main(sys.argv[1:])
