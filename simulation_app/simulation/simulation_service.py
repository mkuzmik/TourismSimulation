import logging

from simulation_app.simulation.db import agent_mapper, simulation_mapper, poi_mapper
from simulation_app.simulation.db.agent_mapper import AgentMapper
from simulation_app.simulation.db.poi_mapper import PoiMapper
from simulation_app.simulation.db.simulation_mapper import SimulationMapper
from simulation_app.simulation.simulation import Simulation

log = logging.getLogger('SimulationService')


class SimulationService:
    def __init__(self,
                 _agent_mapper: AgentMapper,
                 _simulation_mapper: SimulationMapper,
                 _poi_mapper: PoiMapper):
        self.agent_mapper = _agent_mapper
        self.simulation_mapper = _simulation_mapper
        self.poi_mapper = _poi_mapper

    def save_state(self, simulation: Simulation):
        log.debug('Saving simulation state')
        if simulation.id is None:
            self.simulation_mapper.create_simulation(simulation)
        for poi in simulation.pois:
            if poi.id is None:
                self.poi_mapper.create_poi(simulation, poi)
        for agent in simulation.agents:
            if agent.id is None:
                self.agent_mapper.create_agent(agent)
            self.agent_mapper.update_agent_state(agent, simulation.real_time)


INSTANCE = SimulationService(agent_mapper.get_instance(),
                             simulation_mapper.get_instance(),
                             poi_mapper.get_instance())


def get_instance() -> SimulationService:
    global INSTANCE
    return INSTANCE
