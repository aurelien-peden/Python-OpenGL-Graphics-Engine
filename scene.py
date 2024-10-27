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

    def render(self):
        for obj in self.objects:
            obj.render()