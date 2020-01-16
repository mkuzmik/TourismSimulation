import logging

from simulation_app.simulation.model.agent import Agent
from simulation_app.simulation.db import db_connection
from simulation_app.simulation.db.db_connection import DbConnection

log = logging.getLogger('AgentMapper')


class AgentMapper:
    def __init__(self, db: DbConnection):
        self.db = db

    def create_agent(self, agent: Agent):
        log.debug('Adding new agent to DB: %s'.format(agent))
        cursor = self.db.get_cursor()
        cursor.execute('''
        INSERT INTO agent (
            simulation_id, age
        ) VALUES (
            %s,
            %s
        ) RETURNING id;
        ''', (agent.simulation.id, int(agent.age)))
        agent.id = cursor.fetchone()[0]
        cursor.close()

    def update_agent_state(self, agent: Agent, simulation_time: int):
        log.debug('Adding agent state to DB: %s'.format(agent))
        cursor = self.db.get_cursor()
        poi_id = agent.current_poi.id if agent.inside_poi is True else None
        cursor.execute('''
        INSERT INTO agent_spacetime_location (
            agent_id, simulation_id, simulation_time, x, y, point_of_interest_id
        ) VALUES (
            %s, %s, to_timestamp(%s), %s, %s, %s
        );
        ''', (agent.id, agent.simulation.id, simulation_time, agent.posx, agent.posy, poi_id))
        cursor.close()

    def find_all_agents_positions(self):
        log.debug('Fetching agents positions from DB')
        cursor = self.db.get_cursor()
        cursor.execute('''
        SELECT x, y
        FROM agent_spacetime_location
        WHERE simulation_time = (
            SELECT max(simulation_time)
            FROM agent_spacetime_location)
        group by agent_id, x, y
        ''')
        agents = cursor.fetchall()
        fx = lambda x: int((x-510.247) * (-0.66145))
        fy = lambda y: int((y-3522.75) * (-0.304017))
        return [{'x': fx(agent[0]), 'y': fy(agent[1])} for agent in agents]

INSTANCE = AgentMapper(db=db_connection.get_instance())


def get_instance():
    global INSTANCE
    return INSTANCE
