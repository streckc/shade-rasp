
import sqlite3

from os import path

_db_connection = None
_db_cursor = None


def connect_db(location):
    global _db_connection

    if location == ':memory:' or path.isdir(path.dirname(location)):
        _db_connection = sqlite3.connect(location)


def close_db():
    global _db_connection

    if _db_connection is not None:
        _db_connection.close()


def exec_sql(sql, params=[]):
    if not sql:
        return None

    status = True
    data = None
    error = None

    cursor = _get_cursor()
    operation = sql.split(' ')[0].lower()

    try:
        if type(params) == list and len(params) > 0 and type(params[0]) in (list, dict, tuple):
            print('x')
            cursor.executemany(sql, _yield_rows(params))
        else:
            print('y')
            cursor.execute(sql, params)
    except Exception as err:
        error = str(err)
        status = False

    if status == True:
        if operation in ('select',):
            data = cursor.fetchall()
        elif operation in ('insert', 'update', 'delete'):
            _commit()
            data = cursor.rowcount

    return { 'status': status, 'data': data, 'error': error }


def _commit():
    global _db_connection

    if _db_connection is not None:
        _db_connection.commit()


def _get_cursor():
    global _db_connection, _db_cursor

    if _db_cursor is None:
        _db_cursor = _db_connection.cursor()

    return _db_cursor


def _yield_rows(rows):
    for row in rows:
        yield row

