
import json

#from .config import set_config

from .sensor_avahi_browse import _compute_sensor_command
from .sensor_avahi_browse import _parse_avahi_browse_output
from .sensor_avahi_browse import _decode_labels


def test_compute_sensor_command():
    base_command = ['avahi-browse', '--all', '--parsable', '--terminate', '--verbose', '--resolve']

    assert _compute_sensor_command() == base_command


def test_parse_avahi_browse_output():
    output = ''
    with open('test_avahi_browse.txt', 'r') as fin:
        output = fin.read()

    expect = []
    with open('test_avahi_browse.json', 'r') as fin:
        expect = json.load(fin)

    assert _parse_avahi_browse_output(None) == []
    assert _parse_avahi_browse_output('') == []
    assert _parse_avahi_browse_output(output) == expect


def test_decode_labels():
    assert _decode_labels('') == ''
    assert _decode_labels('abc') == 'abc'
    assert _decode_labels('abc\\032abc') == 'abc abc'

