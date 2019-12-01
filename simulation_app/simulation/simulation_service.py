import logging

from simulation_app.simulation.db import agent_mapper, simulation_mapper
from simulation_app.simulation.db.agent_mapper import AgentMapper
from simulation_app.simulation.db.simulation_mapper import SimulationMapper
from simulation_app.simulation.simulation import Simulation

log = logging.getLogger('SimulationService')


class SimulationService:
    def __init__(self, _agent_mapper: AgentMapper, _simulation_mapper: SimulationMapper):
        self.agent_mapper = _agent_mapper
        self.simulation_mapper = _simulation_mapper

    def save_state(self, simulation: Simulation):
        log.debug('Saving simulation state')
        if simulation.id is None:
            self.simulation_mapper.create_simulation(simulation)
        for agent in simulation.agents:
            if agent.id is None:
                self.agent_mapper.create_agent(agent)
            self.agent_mapper.update_agent_state(agent, simulation.real_time)


INSTANCE = SimulationService(agent_mapper.get_instance(), simulation_mapper.get_instance())


def get_instance() -> SimulationService:
    global INSTANCE
    return INSTANCE
