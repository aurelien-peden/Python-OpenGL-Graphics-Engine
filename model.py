import numpy as np
import glm
import pygame as pg


class BaseModel:
    def __init__(self, app, vao_name, texture_id, pos=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rotation = glm.vec3([glm.radians(i) for i in rotation])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()

        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))

        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', texture_id=0, pos=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, pos, rotation, scale)
        self.on_init()

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_0'] = 0
        self.texture.use()

        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

    def update(self):
        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
