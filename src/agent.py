import pyglet

class Agent:

    def __init__(self, posx, posy):

        self.posx = posx
        self.posy = posy
        self.velx = 0
        self.vely = 0
        self.sprite = pyglet.sprite.Sprite(pyglet.image.load('./graphics/Pin.png'), x=self.posx, y=self.posy)

    def draw(self, windowx, windowy):
        self.sprite.x = windowx + self.posx
        self.sprite.y = windowy + self.posy
        self.sprite.draw()

    def update(self, dt):
        self.posx += self.velx * dt
        self.posy += self.vely * dt
