
import json

from .config import set_config

from .sensor_df import _compute_sensor_command
from .sensor_df import _parse_df_output


def test_compute_sensor_command():
    base_command = ['df', '-k']

    assert _compute_sensor_command() == base_command


def test_parse_df_output():
    output = ''
    with open('test_df.txt', 'r') as fin:
        output = fin.read()

    expect = []
    with open('test_df.json', 'r') as fin:
        expect = json.load(fin)

    assert _parse_df_output(None) == []
    assert _parse_df_output('') == []
    assert _parse_df_output(output) == expect

