from .vbo import VBO
from .shader_program import ShaderProgram


class VAO:
    """
    A class used to represent a Vertex Array Object (VAO).
    Attributes
    ----------
    ctx : object
        The context in which the VAO is created.
    vbo : VBO
        The Vertex Buffer Object (VBO) associated with this VAO.
    program : ShaderProgram
        The Shader Program associated with this VAO.
    vaos : dict
        A dictionary storing VAOs for different objects (e.g., 'cube', 'cat').
    Methods
    -------
    __init__(ctx)
        Initializes the VAO with the given context, creates VBO and ShaderProgram instances, 
        and sets up VAOs for predefined objects.
    get_vao(program, vbo)
        Creates and returns a VAO for the given shader program and VBO.
    destroy()
        Destroys the VBO and ShaderProgram instances associated with this VAO.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # Cube
        self.vaos['cube'] = self.get_vao(program=self.program.programs['default'],
                                         vbo=self.vbo.vbos['cube'])

        self.vaos['cat'] = self.get_vao(program=self.program.programs['default'],
                                        vbo=self.vbo.vbos['cat'])

    def get_vao(self, program, vbo):
        """
        Creates and returns a Vertex Array Object (VAO) using the provided program and Vertex Buffer Object (VBO).
        Args:
            program: The shader program to be used with the VAO.
            vbo: An instance of a Vertex Buffer Object containing the vertex data, format, and attributes.
        Returns:
            The created Vertex Array Object (VAO).
        """

        vao = self.ctx.vertex_array(
            program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        """
        Destroys the Vertex Array Object (VAO) by releasing its associated resources.
        This method calls the destroy methods of the Vertex Buffer Object (VBO) and the shader program
        to ensure that all allocated resources are properly released.
        """

        self.vbo.destroy()
        self.program.destroy()
