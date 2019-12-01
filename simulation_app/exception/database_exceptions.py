from simulation_app.exception.app_exception import AppException


class DatabaseConnectionException(AppException):
    def __init__(self):
        AppException.__init__(self)
        self.message = 'Cannot connect to database'
