import pyglet
from pyglet.gl import *

import tuio_rcv

window = pyglet.window.Window(visible=True, resizable=True)

def square(c1):
    #glColor4f(0.23, 0.23, 0.23, 1.0)
    x1, y1 = c1
    x2, y2 = x1 + 10, y1 + 10
    print x1, y1, x2, y2
    pyglet.graphics.draw(4, GL_QUADS, ('v2f', (x1, y1, x1, y2, x2, y2, x2, y1)))

def readinput(dt):
    tuio_rcv.each_frame()

def normalize(x, y):
    return x * window.width, y * window.height 

@window.event
def on_draw():
    background.blit_tiled(0, 0, 0, window.width, window.height)
    for x,y in tuio_rcv.clicks.itervalues():
        y = 1 - y
        square(normalize(x, y))
    tuio_rcv.clicks.clear()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(readinput, 0.001)

    checks = pyglet.image.create(32, 32, pyglet.image.CheckerImagePattern())
    background = pyglet.image.TileableTexture.create_for_image(checks)

    # Enable alpha blending, required for image.blit.
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    pyglet.app.run()
