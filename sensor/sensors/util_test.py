# util_test.py


# Test Display
#   'set_display_timestamp', 'set_display_verbose', 'display', 'display_line',
from .util import display

def test_display(capsys):
    display('Whee')
    captured = capsys.readouterr()
    assert captured.out == 'Whee\n'
    assert captured.err == ''
    display('Whee', warning=True)
    captured = capsys.readouterr()
    assert captured.out == ''
    assert captured.err == 'Whee\n'


# Test Timestamp
from .util import now
from .util import today
from .util import normalize_date
from datetime import datetime

def test_now():
    time = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    assert now() == time

def test_today():
    date = datetime.strftime(datetime.now(), '%Y-%m-%d')
    assert today() == date

def test_normalize_date():
    test_date = '25-09-2018'
    test_format = '%d-%m-%Y'
    test_result = '2018-09-25'
    assert normalize_date(test_date, test_format) == test_result


# Test converstion to list or array
#   'make_list', 'make_array',
from .util import make_list
from .util import make_array

def test_make_list():
    assert make_list('a') == ['a']
    assert make_list(1) == [1]
    assert make_list({ 'a': 'b' }) == [{ 'a': 'b' }]
    assert make_list(['a']) == ['a']
    assert make_list([{ 'a': 'b' }]) == [{ 'a': 'b' }]
    assert make_list(['a', 'b']) == ['a', 'b']
    assert make_list([1, 'b']) == [1, 'b']
    assert make_list([[1, 2], 'b']) == [[1, 2], 'b']

def test_make_list():
    assert make_array('a') == { 'a': None }
    assert make_array(['a']) == { 'a': None }
    assert make_array({ 'a': 'b' }) == { 'a': 'b'}
    assert make_array(['a', 'b']) == { 'a': 'b' }
    assert make_array(['a', 'b', 1, 2]) == { 'a': 'b', 1: 2 }


# Test file content
#   'get_file_content', 'write_file_content'


# Test MD5
from .util import md5

def test_md5_values():
    md_whee = md5('Wheee')
    assert md_whee == 'a365dce63398b13f155896afb19f51b7'
    md_spam = md5('Spam')
    assert md_spam == 'e9dfd31cc505d51fc26975250750deab'

