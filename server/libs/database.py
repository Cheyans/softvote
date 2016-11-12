import pymysql
from time import sleep
from flask import g


def connect(db_credentials: dict):
    if not hasattr(g, 'mysql_connection'):
        g.mysql_connection = _connect_or_wait(db_credentials)
    return g.mysql_connection


def _connect_or_wait(db_credentials: dict):
    connection = None
    attempts = 0
    max_attempts = 10
    sleep_time = 3

    while not connection:
        try:
            connection = pymysql.connect(**db_credentials)
        except pymysql.err.OperationalError:
            if attempts >= max_attempts:
                print('Failed to connect to db after {} seconds'.format(sleep_time * max_attempts))
                raise pymysql.err.OperationalError()
            print('Could not connect to db, sleeping for {}s'.format(sleep_time))
            attempts += 1
            sleep(sleep_time)
    return connection
