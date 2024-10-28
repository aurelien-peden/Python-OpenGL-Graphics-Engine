from model import *

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app

        n, s = 30, 3
        for x in range(-n, n, s):
            for z in range(-n, n, s):
                    self.add_object(Cube(app, texture_id=1, pos=(x, -s, z)))

        self.add_object(Cat(app, texture_id=3, pos=(0, -2, -10), rotation=(-90, 0, 0), scale=(0.3, 0.3, 0.3)))
        

    def render(self):
        for obj in self.objects:
            obj.render()