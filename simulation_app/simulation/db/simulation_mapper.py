import logging

from simulation_app.simulation.db import db_connection
from simulation_app.simulation.db.db_connection import DbConnection
from simulation_app.simulation.simulation import Simulation

log = logging.getLogger('SimulationMapper')


class SimulationMapper:
    def __init__(self, db: DbConnection):
        self.db = db

    def create_simulation(self, simulation: Simulation):
        log.debug('Adding new agent to DB: {}'.format(simulation))
        cursor = self.db.get_cursor()
        cursor.execute('''
        INSERT INTO simulation (
            start_time
        ) VALUES (
            now()
        ) RETURNING id;
        ''')
        simulation.id = cursor.fetchone()[0]
        cursor.close()


INSTANCE = SimulationMapper(db=db_connection.get_instance())


def get_instance():
    global INSTANCE
    return INSTANCE
