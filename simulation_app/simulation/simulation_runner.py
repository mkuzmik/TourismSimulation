import logging
import threading

from simulation_app.exception.simulation_exceptions import *
from simulation_app.simulation import simulation_service
from simulation_app.simulation.simulation import Simulation

log = logging.getLogger('SimulationRunner')


class SimulationRunner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.should_run = True
        self.started = False
        self.simulation = Simulation(2260, 3540, 2260, 3540, 'configs/one_agent/config.yaml')
        self.simulation_service = simulation_service.get_instance()
        log.info('Thread instantiated')

    def stop_gracefully(self):
        log.info('Stop signal sent to thread. Simulation is stopping..')
        self.should_run = False

    def run(self) -> None:
        try:
            self.started = True
            while self.should_run:
                log.info('Running simulation')
                self.simulation.update(1 / 60)
                self.simulation_service.save_state(self.simulation)
        except Exception as ex:
            log.exception(ex)
        finally:
            self.started = False
            log.info('Simulation runner stopped')

    def is_started(self):
        return self.started


RUNNER = None


def run_simulation():
    global RUNNER
    if RUNNER is not None and RUNNER.is_started():
        log.error('Simulation already started')
        raise SimulationAlreadyStartedException()
    RUNNER = SimulationRunner()
    RUNNER.start()


def stop_simulation():
    global RUNNER
    if RUNNER is not None and isinstance(RUNNER, SimulationRunner):
        RUNNER.stop_gracefully()
