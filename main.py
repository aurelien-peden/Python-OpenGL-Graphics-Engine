import pygame as pg
import moderngl as mgl
import sys
from src.model import *
from src.camera import Camera
from src.light import Light
from src.mesh import Mesh
from src.scene import Scene

class GraphicsEngine:
    """
    A class to represent a graphics engine using Pygame and ModernGL.
    Attributes:
    -----------
    WIN_SIZE : tuple
        The size of the window.
    ctx : mgl.Context
        The ModernGL context.
    clock : pg.time.Clock
        The Pygame clock object.a
    time : float
        The current time in seconds.
    delta_time : float
        The time difference between frames.
    light : Light
        The light object in the scene.
    camera : Camera
        The camera object in the scene.
    mesh : Mesh
        The mesh object in the scene.
    scene : Scene
        The scene object.
    Methods:
    --------
    __init__(win_size=(1600, 900)):
        Initializes the graphics engine with the given window size.
    check_events():
        Checks for Pygame events and handles quitting the application.
    render():
        Clears the frame buffer and renders the scene.
    get_time():
        Updates the current time in seconds.
    run():
        The main loop of the graphics engine.
    """
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

        self.light = Light()

        self.camera = Camera(self)

        self.mesh = Mesh(self)

        self.scene = Scene(self)
    
    def check_events(self):
        """
        Handles the event loop for the application.
        This method processes all pending events in the event queue. If a quit event
        (such as closing the window or pressing the ESC key) is detected, it will 
        destroy the mesh, quit Pygame, and exit the program.
        Events handled:
        - QUIT: Triggered when the window is closed.
        - KEYDOWN: Triggered when a key is pressed. Specifically checks for the ESC key.
        Raises:
        - SystemExit: Exits the program when a quit event is detected.
        """

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        """
        Render the current scene.
        This method performs the following steps:
        1. Clears the frame buffer with a specified color.
        2. Renders the scene.
        3. Swaps the display buffers to update the screen with the rendered content.
        """

        # clear frame buffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        """
        Updates the instance's time attribute with the current time in seconds.
        This method retrieves the current time in milliseconds using `pg.time.get_ticks()`
        and converts it to seconds by multiplying by 0.001. The result is then stored
        in the instance's `time` attribute.
        """

        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        """
        Runs the main loop of the application.
        This method continuously executes the following steps:
        1. Retrieves the current time.
        2. Checks for and processes any events.
        3. Updates the camera state.
        4. Renders the current frame.
        5. Regulates the frame rate to 60 frames per second.
        This loop runs indefinitely until the application is terminated.
        """

        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()