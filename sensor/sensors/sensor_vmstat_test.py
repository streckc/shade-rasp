
import json

from .config import set_config

from .sensor_vmstat import _compute_sensor_command
from .sensor_vmstat import _parse_vmstat_output


def test_compute_sensor_command():
    base_command = ['vmstat', '1', '2']

    assert _compute_sensor_command() == base_command


def test_parse_vmstat_output():
    output = ''
    with open('test_vmstat.txt', 'r') as fin:
        output = fin.read()

    expect = []
    with open('test_vmstat.json', 'r') as fin:
        expect = json.load(fin)

    assert _parse_vmstat_output(None) == []
    assert _parse_vmstat_output('') == []
    assert _parse_vmstat_output(output) == expect

