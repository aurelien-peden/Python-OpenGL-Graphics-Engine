import numpy as np
import glm
import pygame as pg


class BaseModel:
    """
    A base model class for rendering 3D objects in an OpenGL context.
    Attributes:
        app (object): The application instance.
        vao_name (str): The name of the Vertex Array Object (VAO).
        texture_id (int): The ID of the texture to be used.
        pos (tuple): The position of the model in 3D space (default is (0, 0, 0)).
        rotation (tuple): The rotation of the model in degrees for each axis (default is (0, 0, 0)).
        scale (tuple): The scale of the model in each axis (default is (1, 1, 1)).
        m_model (glm.mat4): The model matrix.
        vao (object): The VAO associated with the model.
        program (object): The shader program associated with the VAO.
        camera (object): The camera instance from the application.
    Methods:
        update():
            Updates the model's state. This method should be overridden by subclasses.
        get_model_matrix():
            Computes and returns the model matrix based on position, rotation, and scale.
        render():
            Updates the model and renders it using the associated VAO.
    """

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

    def update(self):
        pass

    def get_model_matrix(self):
        """
        Generates and returns the model matrix for the object.
        The model matrix is computed by applying translation, rotation, 
        and scaling transformations in that order. The transformations 
        are applied based on the object's position, rotation, and scale 
        attributes.
        Returns:
            glm.mat4: The resulting model matrix after applying the 
                  transformations.
        """

        m_model = glm.mat4()

        m_model = glm.translate(m_model, self.pos)

        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))

        m_model = glm.scale(m_model, self.scale)
        return m_model
    
    def render(self):
        """
        Renders the model by updating its state and invoking the render method
        of the Vertex Array Object (VAO).
        This method first calls the `update` method to ensure the model's state
        is current, and then it calls the `render` method of the VAO to draw
        the model.
        """

        self.update()
        self.vao.render()


class Cube(BaseModel):
    """
    A class representing a 3D cube model in an OpenGL graphic engine.
    Attributes:
        app (App): The application instance.
        vao_name (str): The name of the Vertex Array Object (VAO) for the cube.
        texture_id (int): The ID of the texture to be used for the cube.
        pos (tuple): The position of the cube in 3D space.
        rotation (tuple): The rotation of the cube in 3D space.
        scale (tuple): The scale of the cube in 3D space.
        texture (Texture): The texture object associated with the cube.
        program (Program): The shader program used for rendering the cube.
    Methods:
        __init__(app, vao_name='cube', texture_id=0, pos=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
            Initializes the Cube instance with the given parameters and calls the on_init method.
        on_init():
            Initializes the cube's texture and shader program uniforms.
        update():
            Updates the cube's texture and shader program uniforms based on the current camera position and view.
    """

    def __init__(self, app, vao_name='cube', texture_id=0, pos=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, pos, rotation, scale)
        self.on_init()

    def on_init(self):
        """
        Initializes the model by setting up the texture, shader program, and 
        various transformation and lighting matrices.
        This method performs the following actions:
        - Retrieves the texture associated with the model and binds it to the shader program.
        - Sets the projection, view, and model matrices in the shader program.
        - Sets the light properties (position, ambient, diffuse, and specular intensities) in the shader program.
        Attributes:
        - self.texture: The texture object associated with the model.
        - self.program: The shader program used for rendering.
        - self.camera: The camera object providing projection and view matrices.
        - self.m_model: The model matrix for the object.
        - self.app.light: The light object providing lighting properties.
        """

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
        """
        Updates the model's state by applying the current texture and writing
        the camera position, view matrix, and model matrix to the shader program.
        This method performs the following steps:
        1. Uses the current texture.
        2. Writes the camera's position to the shader program.
        3. Writes the camera's view matrix to the shader program.
        4. Writes the model's transformation matrix to the shader program.
        """

        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

class Cat(BaseModel):
    """
    A class representing a Cat model in the OpenGL graphic engine.
    Attributes:
        app (App): The application instance.
        vao_name (str): The name of the Vertex Array Object (VAO) for the cat model.
        texture_id (str): The identifier for the texture used by the cat model.
        pos (tuple): The position of the cat model in 3D space.
        rotation (tuple): The rotation of the cat model in 3D space.
        scale (tuple): The scale of the cat model in 3D space.
        texture (Texture): The texture object associated with the cat model.
        program (Program): The shader program used for rendering the cat model.
    Methods:
        __init__(app, vao_name='cat', texture_id='cat', pos=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
            Initializes the Cat model with the given parameters and calls the on_init method.
        on_init():
            Initializes the texture and shader program uniforms for the cat model.
        update():
            Updates the texture and shader program uniforms for the cat model.
    """

    def __init__(self, app, vao_name='cat', texture_id='cat', pos=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, pos, rotation, scale)
        self.on_init()

    def on_init(self):
        """
        Initializes the model by setting up the texture, shader program, and lighting.
        This method performs the following tasks:
        - Retrieves the texture from the application's mesh texture list using the texture ID.
        - Sets the texture unit for the shader program.
        - Uses the texture.
        - Writes the projection, view, and model matrices to the shader program.
        - Writes the light's position and intensity (ambient, diffuse, and specular) to the shader program.
        """

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
        """
        Updates the model's state by applying the current texture and writing
        the camera position, view matrix, and model matrix to the shader program.
        This method performs the following steps:
        1. Activates the texture associated with the model.
        2. Writes the camera's position to the shader program.
        3. Writes the camera's view matrix to the shader program.
        4. Writes the model's transformation matrix to the shader program.
        """

        self.texture.use()
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)