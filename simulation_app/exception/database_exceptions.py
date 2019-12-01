from simulation_app.exception.app_exceptions import FatalException


class DatabaseConnectionException(FatalException):
    def __init__(self):
        FatalException.__init__(self)
        self.message = 'Cannot connect to database'
