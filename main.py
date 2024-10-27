import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene

class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        # Init pygame modules
        pg.init()
        self.WIN_SIZE = win_size

        # Configure OpenGL attributes
        # Set OpenGL 3.3 core profile
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)

        pg.event.set_grab(True) # grab the mouse
        pg.mouse.set_visible(False) # hide the mouse cursor

        # Detect and use existing OpenGL context
        self.ctx = mgl.create_context()
        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE) # enable depth test and culling of back faces

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0

        # light
        self.light = Light()

        # camera
        self.camera = Camera(self)

        self.mesh = Mesh(self)

        # scene
        #self.scene = Triangle(self)
        self.scene = Scene(self)
    
    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        # clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()