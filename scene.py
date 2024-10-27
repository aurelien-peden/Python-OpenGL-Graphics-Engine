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
        self.add_object(Cube(app))
        self.add_object(Cube(app, texture_id=1, pos=(-4, 0, 0), rotation=(45, 0, 0), scale=(1, 4, 1)))
        self.add_object(Cube(app, texture_id=2, pos=(4, 0, 0), rotation=(0, 45, 0), scale=(1, 4, 1)))

    def render(self):
        for obj in self.objects:
            obj.render()