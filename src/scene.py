from .model import *

class Scene:
    """
    A class to represent a 3D scene in an OpenGL graphic engine.
    Attributes
    ----------
    app : object
        The application instance that the scene belongs to.
    objects : list
        A list to store objects in the scene.
    Methods
    -------
    __init__(app):
        Initializes the scene with the given application instance.
    add_object(obj):
        Adds an object to the scene.
    load():
        Loads the initial objects into the scene.
    render():
        Renders all objects in the scene.
    """

    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        """
        Adds an object to the scene.
        Parameters:
        obj (Object): The object to be added to the scene.
        """

        self.objects.append(obj)

    def load(self):
        """
        Loads the scene with objects.
        This method initializes the scene by adding multiple Cube objects in a grid pattern
        and a single Cat object with specific position, rotation, and scale.
        The grid of Cube objects is created with the following parameters:
        - n: The range limit for the grid (default is 30).
        - s: The step size for the grid (default is 3).
        The Cat object is added with the following parameters:
        - texture_id: The texture identifier for the Cat object (default is 3).
        - pos: The position of the Cat object (default is (0, -2, -10)).
        - rotation: The rotation of the Cat object (default is (-90, 0, 0)).
        - scale: The scale of the Cat object (default is (0.3, 0.3, 0.3)).
        Returns:
            None
        """

        app = self.app

        n, s = 30, 3
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                    self.add_object(Cube(app, texture_id=1, pos=(x, -s, z)))

        self.add_object(Cube(app, texture_id=0, pos=(15, 5, 10), rotation=(0, 0, 0), scale=(4, 1, 4)))
        self.add_object(Cube(app, texture_id=2, pos=(10, 0, 10), rotation=(-45, 30, 0), scale=(2, 1, 1)))
        self.add_object(Cat(app, texture_id=3, pos=(0, -2, -10), rotation=(-90, 0, -90), scale=(0.3, 0.3, 0.3)))
        

    def render(self):
        """
        Renders all objects in the scene.
        This method iterates through all objects in the scene and calls their
        render method to display them.
        """

        for obj in self.objects:
            obj.render()