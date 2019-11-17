import time
import threading
import logging
from app.simulation.simulation import Simulation

from app.exception.simulation_exceptions import *

log = logging.getLogger('SimulationRunner')


class SimulationRunner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.should_run = True
        self.simulation = Simulation(2260, 3540, 2260, 3540, 'configs/default/config.yaml')
        log.info('Thread instantiated')

    def stop_gracefully(self):
        log.info('Stop signal sent to thread. Simulation is stopping..')
        self.should_run = False

    def run(self) -> None:
        try:
            while self.should_run:
                log.info('Running simulation')
                self.simulation.update(1/60)
        except Exception as ex:
            log.error('Stopped because of {}'.format(ex))
        finally:
            log.info('Simulation runner stopped')


RUNNER = None


def run_simulation():
    global RUNNER
    if RUNNER is not None and isinstance(RUNNER, SimulationRunner):
        log.error('Simulation already started')
        raise SimulationAlreadyStartedException()
    RUNNER = SimulationRunner()
    RUNNER.start()


def stop_simulation():
    global RUNNER
    if RUNNER is not None and isinstance(RUNNER, SimulationRunner):
        RUNNER.stop_gracefully()

