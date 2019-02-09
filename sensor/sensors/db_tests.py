
from .db import connect_db
from .db import exec_sql
from .db import close_db

connect_db(':memory:')


def _create_test_tables():
    exec_sql('create table test_table (id integer primary key, key text, value text)')


def _drop_test_tables():
    exec_sql('drop table test_table')


def test_no_sql_statment():
    assert exec_sql('') == None


def test_sql_create_and_drop():
    result = exec_sql('create table test_table (id integer primary key, key text, value text)')
    assert result == { 'status': True, 'error': None, 'data': None }

    result = exec_sql('select name from sqlite_master where type="table"')
    assert result == { 'status': True, 'error': None, 'data': [('test_table',)] }

    result = exec_sql('drop table test_table')
    assert result == { 'status': True, 'error': None, 'data': None }

    result = exec_sql('select name from sqlite_master where type="table"')
    assert result == { 'status': True, 'error': None, 'data': [] }

    result = exec_sql('drop table no_test_table')
    assert result == { 'status': False, 'error': 'no such table: no_test_table', 'data': None }

    result = exec_sql('select name from sqlite_master where type="table"')
    assert result == { 'status': True, 'error': None, 'data': [] }


def test_sql_insert_select():
    _create_test_tables()

    result = exec_sql('insert into test_table (key, value) values ("key one", "value one")')
    assert result == { 'status': True, 'error': None, 'data': 1 }

    result = exec_sql('insert into test_table (key, value) values ("key two", "value two")')
    assert result == { 'status': True, 'error': None, 'data': 1 }

    result = exec_sql('select * from test_table')
    assert result == { 'status': True, 'error': None, 'data': [
        (1, 'key one', 'value one'),
        (2, 'key two', 'value two')
    ]}

    _drop_test_tables()


def test_sql_insert_select_binds():
    _create_test_tables()

    data = ['key one', 'value one']
    result = exec_sql('insert into test_table (key, value) values (?, ?)', data)
    assert result == { 'status': True, 'error': None, 'data': 1 }

    data = {'key': 'key two', 'val': 'value two'}
    result = exec_sql('insert into test_table (key, value) values (:key, :val)', data)
    assert result == { 'status': True, 'error': None, 'data': 1 }

    data = [
        ('key three', 'value three'),
        ('key four', 'value four'),
        ('key five', 'value five')
    ]
    result = exec_sql('insert into test_table (key, value) values (?, ?)', data)
    assert result == { 'status': True, 'error': None, 'data': 3 }

    result = exec_sql('select * from test_table')
    assert result == { 'status': True, 'error': None, 'data': [
        (1, 'key one', 'value one'),
        (2, 'key two', 'value two'),
        (3, 'key three', 'value three'),
        (4, 'key four', 'value four'),
        (5, 'key five', 'value five')
    ]}

    _drop_test_tables()

