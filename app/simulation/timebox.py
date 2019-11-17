import datetime

import pyglet


class Timebox:
    def __init__(self, timestamp, window_width, window_height):
        self.timestamp = timestamp
        self.x = window_width
        self.y = window_height

        self.label = None
        self.labelShadow = None

    def to_string(self):
        return datetime.datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')

    def update(self, dt):
        self.timestamp += dt

    def draw(self, x, y):
        self.label = self.label = pyglet.text.Label(
            self.to_string(), color=(255, 255, 255, 255),
            font_name='Calibri', font_size=12,
            x=x - 8, y=y - 8,
            anchor_x='right', anchor_y='top')

        self.labelShadow = pyglet.text.Label(
            self.to_string(), font_name='Calibri',
            font_size=12, x=x - 7, color=(0, 0, 0, 255),
            y=y - 9, anchor_x='right', anchor_y='top')

        self.labelShadow.draw()
        self.label.draw()
