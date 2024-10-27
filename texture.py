import pygame as pg
import moderngl as mgl

class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture('textures/img.jpg')
        self.textures[1] = self.get_texture('textures/img_1.jpg')
        self.textures[2] = self.get_texture('textures/img_2.jpg')

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, False, True) # flip image vertically because the y-axis is inverted in pygame
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, 'RGB'))
        return texture
    
    def destroy(self):
        for texture in self.textures.values():
            texture.release()