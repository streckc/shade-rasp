
from datetime import datetime

from time import sleep

from .cron import schedule_job
from .cron import start_scheduler
from .cron import stop_scheduler
from .cron import run_pending_jobs
from .cron import _load_job_queue
from .cron import _scheduled_jobs
from .cron import _job_run_queue
from .cron import _compute_times
from .cron import _can_run_now


def test_compute_times():
    assert _compute_times('') == [[], [], [], [], []]
    assert _compute_times('* * * * *') == [list(range(60)), list(range(24)), list(range(31)), list(range(12)), list(range(52))]
    assert _compute_times('*') == [list(range(60)), list(range(24)), list(range(31)), list(range(12)), list(range(52))]
    assert _compute_times('1 2 3 4 5') == [[1], [2], [3], [4], [5]]
    assert _compute_times('1,2 2,3 3,4 4,5 5,6') == [[1, 2], [2, 3], [3, 4], [4, 5], [5, 6]]
    assert _compute_times('*/5') == [list(range(0, 60, 5)), list(range(24)), list(range(31)), list(range(12)), list(range(52))]
    assert _compute_times('5') == [[5], list(range(24)), list(range(31)), list(range(12)), list(range(52))]
    assert _compute_times('5,2') == [[5, 2], list(range(24)), list(range(31)), list(range(12)), list(range(52))]


def test_bad_params():
    assert _can_run_now() == False
    assert _can_run_now({}) == False
    assert _can_run_now([]) == False
    assert _can_run_now(True) == False
    assert _can_run_now('') == False
    assert _can_run_now('spam') == False
    assert _can_run_now('* * * * * *') == False


def test_all_asteriks():
    assert _can_run_now('*') == True
    assert _can_run_now('* *') == True
    assert _can_run_now('* * *') == True
    assert _can_run_now('* * * *') == True
    assert _can_run_now('* * * * *') == True


def test_minute_values():
    now = datetime.now()
    minute = int(now.strftime('%M'))
    assert _can_run_now('{}'.format((minute + 5) % 60)) == False
    assert _can_run_now('{},{}'.format(minute, (minute + 1) % 60)) == True


def _phantom_func(params=None):
    if params is None:
        print('no params')
    else:
        print(params)


def test_schedule_job():
    now = datetime.now()
    hour = int(now.strftime('%H'))
    
    schedule_job('', 'arp_scan', _phantom_func, {})
    assert len(_scheduled_jobs) == 0
    schedule_job('*', 'arp_scan', _phantom_func)
    assert len(_scheduled_jobs) == 1
    schedule_job('*/5', 'not_arp_scan', _phantom_func, { 'test': 'one' })
    assert len(_scheduled_jobs) == 2
    schedule_job('* {}'.format(hour), 'not_arp_scan', _phantom_func, { 'test': 'two' })
    assert len(_scheduled_jobs) == 3


def test_load_job_queue():
    assert len(_scheduled_jobs) == 3
    now = datetime.now()
    _load_job_queue()
    if int(now.strftime('%M')) % 5 == 0:
        assert len(_job_run_queue) == 3
    else:
        assert len(_job_run_queue) == 2

    # reload will not load jobs already pending
    _load_job_queue()
    if int(now.strftime('%M')) % 5 == 0:
        assert len(_job_run_queue) == 3
    else:
        assert len(_job_run_queue) == 2


def test_run_pending_jobs():
    num_jobs = len(_job_run_queue)
    assert run_pending_jobs() == { 'time': 0, 'jobs': num_jobs }
    assert len(_job_run_queue) == 0
    assert run_pending_jobs() == { 'time': 0, 'jobs': 0 }
    assert len(_job_run_queue) == 0


def test_start_stop_scheduler():
    assert len(_job_run_queue) == 0
    start_scheduler()
    now = datetime.now()
    secs = 65 - now.time().second
    print('sleeping: {}'.format(secs))
    sleep(secs)
    stop_scheduler()
    if (now.time().minute + 1) % 5 == 0:
        assert len(_job_run_queue) == 3
    else:
        assert len(_job_run_queue) == 2

