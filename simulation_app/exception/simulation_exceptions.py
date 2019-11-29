from simulation_app.exception.app_exception import AppException


class SimulationAlreadyStartedException(AppException):
    def __init__(self):
        AppException.__init__(self)
        self.message = 'Simulation is already in progress. You cannot start another one.'
