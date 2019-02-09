
import json

from .config import get_config_value

from .db import connect_db
from .db import exec_sql
from .db import close_db

from .util import log_message


def init_cache(directory):
    location = '{}/{}.db'.format(get_config_value('environment.root', '/tmp'), directory)

    log_message('Database: {}'.format(location), 'config_data')
    connect_db(location)

    exec_sql(('CREATE TABLE IF NOT EXISTS cache ('
              'id INTEGER PRIMARY KEY, '
              'ts DATETIME DEFAULT CURRENT_TIMESTAMP, '
              'data TEXT, '
              'sent INTEGER)'))


def close_cache():
    close_db()


def clear_cache():
    exec_sql('DELETE FROM cache WHERE sent > 0')


def store_data(data):
    exec_sql('INSERT INTO cache (data, sent) VALUES (?, 0)', [json.dumps(data)])


def send_data(host=None, port=None):
    return None

