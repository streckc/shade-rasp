import copy
import datetime
import hashlib
import os
import sys

display_verbose = False
display_timestamp = False

# Returns current time in YYYY-mm-dd HH:MM:SS
def now():
    return(datetime.datetime.strftime(datetime.datetime.now(),
                                      '%Y-%m-%d %H:%M:%S'))


# Returns current date in YYYY-mm-dd
def today():
    return(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))


# Converts provided date string and format into YYYY-mm-dd
def normalize_date(date, date_format='%m-%d-%Y'):
    return datetime.datetime.strptime(date, date_format).strftime('%Y-%m-%d')


def set_display_timestamp(val=True):
    global display_timestamp
    display_timestamp = val


def set_display_verbose(val=True):
    global display_verbose
    display_verbose = val


def display(message='', warning=False, error=False, verbose=False):
    global display_log, display_timestamp, display_verbose

    date = ''
    if display_timestamp:
        date = str(now())+' '

    if not verbose or (verbose and display_verbose):
        if isinstance(message, list):
            for msg in message:
                display_line(date+msg, error=(error or warning))
        else:
            display_line(date+message, error=(error or warning))

    if error:
        sys.exit(1)


def display_line(message, error):
    if error:
        sys.stderr.write(message+'\n')
        sys.stderr.flush()
    else:
        sys.stdout.write(message+'\n')
        sys.stdout.flush()


def log_message(message, key, filename=None):
    global _log_filename

    date = str(now())

    if filename is None:
        filename = _log_filename
    else:
        _log_filename = filename

    with open(filename, 'a+') as fout:
        fout.write('{} {} {}\n'.format(date, key, message))


def md5(value):
    return(hash_value(value, 'md5'))


def hash_value(value, algorithm='md5'):
    h = hashlib.new(algorithm)
    h.update(value.encode('ascii'))
    return(h.hexdigest())


def make_list(value):
    if not type(value) is list:
        return [value]
    else:
        return value


def make_array(value):
    if type(value) is dict:
        return value

    elif type(value) is list:
        result = {}
        length = len(value)
        for x in range(0, length, 2):
            if x + 1 >= length:
                result[value[x]] = None
            else:
                result[value[x]] = value[x + 1]
        return result

    else:
        return { value: None }


def deep_merge(one, two):
    result = copy.deepcopy(one)

    for key in two:
        if key not in one:
            result[key] = two[key]
        elif type(one[key]) is dict and type(two[key]) is dict:
            result[key] = deep_merge(one[key], two[key])
        elif type(one[key]) is list and type(two[key]) is list:
            result[key].extend(two[key])
        else:
            result[key] = two[key]

    return result


def get_file_content(filename):
    content = ''

    with open(filename, 'r') as audit_in:
        content = audit_in.read().strip()

    return content


def write_file_content(filename, content):
    with open(filename, 'w') as audit_out:
        audit_out.write(content.rstrip() + '\n')


