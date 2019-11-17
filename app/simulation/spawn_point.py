from random import randint

import pyglet

from app.simulation.agent import Agent
from app.simulation.poilabel import PoiLabel

import logging

log = logging.getLogger('SpawnPoint')


class SpawnPoint:

    def __init__(self, x, y, name, agents_per_min, bus_frequency, bus_average_number_of_passengers):
        self.x = x
        self.y = y
        self.name = name
        self.is_end_point = True

        # how many agents arrives on foot in one minute
        self.agents_per_min = agents_per_min
        self.agents_frequency = 60.0 / agents_per_min
        self.last_foot_agent = 0

        # how often bus/train arrives (in config in minutes, so multiply times 60)
        self.bus_frequency = bus_frequency * 60
        self.last_bus = -1
        self.bus_average_number_of_passengers = bus_average_number_of_passengers

        self.img = None
        self.sprite = None
        self.label = PoiLabel(name, x, y)
        self.time_needed = 0

    @classmethod
    def from_dict(cls, name, attributes):
        required_all = ["x", "y", "agents_per_min", "bus_frequency", "bus_average_number_of_passengers"]
        for required in required_all:
            if required not in attributes.keys():
                raise ValueError("Required key in spawn points config file not found: {}".format(required))

        if name == "" or name is None:
            raise ValueError("Name can't be empty")
        attributes["name"] = name

        return SpawnPoint(**attributes)

    def draw(self, windowx, windowy):
        if self.sprite is None:
            self.sprite = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
        if self.img is None:
            self.img = pyglet.image.load('./graphics/Spawn.png')
            self.img.anchor_x = self.img.width // 2
            self.img.anchor_y = self.img.height // 2
        self.sprite.x = windowx + self.x
        self.sprite.y = windowy + self.y
        self.sprite.draw()
        self.label.draw(self.sprite.x, self.sprite.y)

    def _spawn_agents(self, simulation, agents_amount):
        for _ in range(agents_amount):
            simulation.agents.append(Agent.generate(simulation, self.x, self.y, self))

    def _agents_in_bus(self, simulation):
        agents_amount = self.bus_average_number_of_passengers + randint(-1, 1)
        log.debug("Bus arrived, point: {}, new agents: {}".format(self.name, agents_amount))
        return agents_amount

    def update(self, simulation_delta_time, simulation):
        # spawn at start of simulation
        if self.last_bus == -1:
            self._spawn_agents(simulation, self._agents_in_bus(simulation))

        # check how many buses/trains arrived from last time it was checked
        self.last_bus += simulation_delta_time
        while self.last_bus >= self.bus_frequency:
            self._spawn_agents(simulation, self._agents_in_bus(simulation))
            self.last_bus -= self.bus_frequency

        # spawn agents that arrived on foot
        self.last_foot_agent += simulation_delta_time
        agents_amount = 0
        while self.last_foot_agent >= self.agents_frequency:
            self.last_foot_agent -= self.agents_frequency
            agents_amount += randint(1, 2)
        self._spawn_agents(simulation, agents_amount)
