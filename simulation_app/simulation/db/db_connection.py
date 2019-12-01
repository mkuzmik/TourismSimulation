import psycopg2

from simulation_app.exception.database_exceptions import *


class DbConnection:
    def __init__(self, host, database, username, password):
        try:
            self.connection = psycopg2.connect(host=host,
                                               database=database,
                                               user=username,
                                               password=password)
            self.connection.autocommit = True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            raise DatabaseConnectionException()

    def get_cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()


# TODO config to file
INSTANCE = DbConnection(host='tourism_database',
                        database='tourism',
                        username='root',
                        password='admin')


def get_instance():
    global INSTANCE
    return INSTANCE
