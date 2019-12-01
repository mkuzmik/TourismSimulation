import logging

from simulation_app.simulation.agent import Agent
from simulation_app.simulation.db import db_connection
from simulation_app.simulation.db.db_connection import DbConnection

log = logging.getLogger('AgentMapper')


class AgentMapper:
    def __init__(self, db: DbConnection):
        self.db = db

    def create_agent(self, agent: Agent):
        log.debug('Adding new agent to DB: {}'.format(agent))
        cursor = self.db.get_cursor()
        cursor.execute('''
        INSERT INTO agent (
            simulation_id, age
        ) VALUES (
            {},
            {}
        ) RETURNING id;
        '''.format(agent.simulation.id, agent.age))
        agent.id = cursor.fetchone()[0]
        cursor.close()

    def update_agent_state(self, agent: Agent, simulation_time: int):
        log.debug('Adding agent state to DB: {}'.format(agent))
        cursor = self.db.get_cursor()
        cursor.execute('''
        INSERT INTO agent_spacetime_location (
            agent_id, simulation_time, x, y
        ) VALUES (
            {}, to_timestamp({}), {}, {}
        );
        '''.format(agent.id, simulation_time, agent.posx, agent.posy))
        cursor.close()


INSTANCE = AgentMapper(db=db_connection.get_instance())


def get_instance():
    global INSTANCE
    return INSTANCE
