
from threading import Lock
from threading import Thread

from copy import deepcopy

from datetime import datetime

from time import sleep

_scheduler_run = False
_thread_lock = Lock()

_scheduled_jobs = []
_job_run_queue = []
_last_poll = None
_blank_times = [[], [], [], [], []]


def schedule_job(schedule, name, func=None, params=None):
    global _scheduled_jobs, _blank_times
    times = _compute_times(schedule)

    if not times or times == _blank_times:
        return False

    _scheduled_jobs.append({
        'name': name,
        'times': times,
        'func': func,
        'params': params
    })

    return True


def _scheduler(args):
    global _scheduler_run, _thread_lock
    lastload = datetime.now().time().minute

    while _scheduler_run:
        while _scheduler_run and datetime.now().time().minute == lastload:
            sleep(1)

        if _scheduler_run:
            _thread_lock.acquire()
            _load_job_queue()
            _thread_lock.release()
            lastload = datetime.now().time().minute


def start_scheduler():
    global _scheduler_run, _thread_lock
    _thread_lock.acquire()
    _scheduler_run = True
    _thread_lock.release()
    t = Thread(target=_scheduler, args=(2,))
    t.start()
    return False


def stop_scheduler():
    global _scheduler_run, _thread_lock
    _thread_lock.acquire()
    _scheduler_run = False
    _thread_lock.release()
    return False


def run_pending_jobs():
    global _job_run_queue
    now = datetime.now()
    num_jobs = 0
    data = []

    num_jobs = len(_job_run_queue)
    for j in range(num_jobs):
        job = _job_run_queue[0]
        data.append(job['func'](job['params']))
        _thread_lock.acquire()
        del(_job_run_queue[0])
        _thread_lock.release()

    return {
        'time': int((datetime.now() - now).total_seconds()),
        'jobs': num_jobs,
        'data': data
    }


def _load_job_queue():
    global _scheduled_jobs, _job_run_queue

    in_job_queue = [j['name'] for j in _job_run_queue]

    for job in _scheduled_jobs:
        if job['name'] not in in_job_queue and _can_run_now(job['times']):
            _job_run_queue.append({
                'name': job['name'],
                'func': job['func'],
                'params': job['params']
            })

    return True


def _can_run_now(cron=''):
    global _blank_times

    times = deepcopy(_blank_times)

    if not cron:
        return False
    elif type(cron) is str:
        times = _compute_times(cron)
    elif type(cron) is not list:
        return False
    elif len(cron) != 5:
        return False
    else:
        for i in range(5):
            if type(cron[i]) is not list:
                return False
        times = cron

    now = datetime.now()
    current = now.strftime('%M %H %d %m %w').split(' ')

    for i in range(5):
        if int(current[i]) not in times[i]:
            return False

    return True


def _compute_times(cron):
    ranges = (60, 24, 31, 12, 52)
    no_times = [[], [], [], [], []]
    times = [[], [], [], [], []]

    if type(cron) is not str or not cron:
        return no_times

    items = cron.split(' ')

    if len(items) > 5:
        return no_times

    for i in range(len(items)):
        for item in items[i].split(','):
            if item == '*':
                times[i].extend(list(range(ranges[i])))
            elif item[:2] == '*/':
                try:
                    (asterisk, minutes) = item.split('/')
                    times[i].extend(list(range(0, ranges[i], int(minutes))))
                except:
                    return no_times
            else:
                try:
                    times[i].append(int(item))
                except:
                    return no_times

    for i in range(len(items), 5):
        times[i].extend(list(range(ranges[i])))

    return times

