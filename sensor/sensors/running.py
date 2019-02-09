
from subprocess import run
from subprocess import PIPE


def run_os_command(command):
    result = run(command, stdout=PIPE, stderr=PIPE)

    return {
        'output': result.stdout.decode('ascii'),
        'error': result.stderr.decode('ascii')
    }
