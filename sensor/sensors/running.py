
from subprocess import run
from subprocess import PIPE
from subprocess import TimeoutExpired


def run_os_command(command, timeout=600):
    output = ''
    error = ''
    exception = ''

    try:
        result = run(command, stdout=PIPE, stderr=PIPE, timeout=int(timeout))
        output = result.stdout.decode('ascii')
        error = result.stderr.decode('ascii')
    except TimeoutExpired as err:
        exception = 'subprocess timed out ({}s)'.format(timeout)

    return { 'output': output, 'error': error, 'except': exception }
