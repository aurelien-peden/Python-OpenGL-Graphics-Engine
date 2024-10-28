from vao import VAO
from texture import Texture


class Mesh:
    """
    Mesh class represents a 3D mesh object in the OpenGL graphic engine.
    Attributes:
        app (App): The application instance that contains the OpenGL context.
        vao (VAO): The Vertex Array Object associated with the mesh.
        texture (Texture): The texture associated with the mesh.
    Methods:
        __init__(app):
            Initializes the Mesh object with the given application context.
        destroy():
            Destroys the VAO and texture associated with the mesh to free up resources.
    """

    def __init__(self, app):
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app.ctx)

    def destroy(self):
        """
        Releases the resources associated with the mesh.
        This method destroys the Vertex Array Object (VAO) and the texture
        associated with the mesh to free up GPU resources.
        """
        
        self.vao.destroy()
        self.texture.destroy()