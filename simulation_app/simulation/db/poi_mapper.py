import logging

from simulation_app.simulation.db import db_connection
from simulation_app.simulation.db.db_connection import DbConnection
from simulation_app.simulation.point_of_interest import PointOfInterest
from simulation_app.simulation.simulation import Simulation

log = logging.getLogger('PoiMapper')


class PoiMapper:
    def __init__(self, db: DbConnection):
        self.db = db

    def create_poi(self, simulation: Simulation, poi: PointOfInterest):
        log.debug('Adding new POI to DB: {}'.format(poi))
        cursor = self.db.get_cursor()
        cursor.execute('''
        INSERT INTO point_of_interest (
            simulation_id, name, x_location, y_location, type
        ) VALUES (
            %s, %s, %s, %s, %s
        ) RETURNING id;
        ''', (simulation.id, poi.name, poi.x, poi.y, poi.type))
        poi.id = cursor.fetchone()[0]
        cursor.close()


INSTANCE = PoiMapper(db=db_connection.get_instance())


def get_instance():
    global INSTANCE
    return INSTANCE
