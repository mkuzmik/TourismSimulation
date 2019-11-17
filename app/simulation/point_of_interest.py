from datetime import datetime
from time import strptime

import pyglet

from app.simulation.poilabel import PoiLabel
from app.simulation.poilabelclosed import PoiLabelClosed


class PointOfInterest:

    def __init__(self, x, y, name, attractiveness, price, people_limit, time_needed, time_open, time_close, poi_type):
        self.x = x
        self.y = y
        self.name = name
        self.is_end_point = False

        self.attractiveness = attractiveness
        self.price = price
        self.people_limit = people_limit
        self.time_needed = time_needed
        self.time_open = time_open
        self.time_close = time_close
        self.type = poi_type

        self.img = None
        self.imgClosed = None
        self.sprite = None

        self.labelOpen = PoiLabel(name, x, y)
        self.labelClosed = PoiLabelClosed(name, x, y)
        self.label = self.labelOpen

    @classmethod
    def from_dict(cls, name, attributes):
        required_all = ["x", "y", "attractiveness", "price", "time_needed", "poi_type"]
        for required in required_all:
            if required not in attributes.keys():
                raise ValueError("Required key in pois config file not found: {}".format(required))

        if name == "" or name is None:
            raise ValueError("Name can't be empty")
        attributes["name"] = name

        return PointOfInterest(**attributes)

    def _time_from_timestamp(self, timestamp):
        tmp = datetime.fromtimestamp(timestamp)
        return (tmp.hour * 60) + tmp.minute

    def _time_from_string(self, time_string):
        tmp = strptime(time_string, '%H:%M')
        return (tmp.tm_hour * 60) + tmp.tm_min

    def update(self, timestamp):
        if self._time_from_timestamp(timestamp) < self._time_from_string(self.time_open) or \
                self._time_from_timestamp(timestamp) > self._time_from_string(self.time_close):
            self.sprite = pyglet.sprite.Sprite(self.imgClosed, x=self.x, y=self.y)
            self.label = self.labelClosed
        else:
            self.sprite = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
            self.label = self.labelOpen

    def draw(self, windowx, windowy):
        if self.img is None:
            self.img = pyglet.image.load('./graphics/POI.png')
            self.img.anchor_x = self.img.width // 2
            self.img.anchor_y = self.img.height // 2
        if self.imgClosed is None:
            self.imgClosed = pyglet.image.load('./graphics/POI_closed.png')
            self.imgClosed.anchor_x = self.img.width // 2
            self.imgClosed.anchor_y = self.img.height // 2
        if self.sprite is None:
            self.sprite = pyglet.sprite.Sprite(self.img, x=self.x, y=self.y)
        self.sprite.x = windowx + self.x
        self.sprite.y = windowy + self.y
        self.sprite.draw()
        self.label.draw(self.sprite.x, self.sprite.y)
