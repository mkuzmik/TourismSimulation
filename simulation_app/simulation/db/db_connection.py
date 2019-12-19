import logging
import time

import psycopg2

from simulation_app.exception.database_exceptions import *

log = logging.getLogger('AgentMapper')


class DbConnection:
    def __init__(self, host, database, username, password):
        success = False
        retries = 10
        while success is False and retries > 0:
            try:
                self.connection = psycopg2.connect(host=host,
                                                   database=database,
                                                   user=username,
                                                   password=password)
                self.connection.autocommit = True
                success = True
            except Exception as error:
                print(error)
                retries -= 1
                log.error('DB connection error. Retrying in 2 seconds')
                time.sleep(2)

        if success is False:
            log.error('Max limit of retires reached..')
            raise DatabaseConnectionException()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()


# TODO config to file
INSTANCE = DbConnection(host='127.0.0.1',
                        database='tourism',
                        username='root',
                        password='admin')


def get_instance():
    global INSTANCE
    return INSTANCE
