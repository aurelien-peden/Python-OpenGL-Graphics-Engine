

class ShaderProgram:
    """
    ShaderProgram is a class that manages shader programs in an OpenGL context.
    Attributes:
        ctx: The OpenGL context.
        programs: A dictionary that stores shader programs.
    Methods:
        __init__(ctx):
            Initializes the ShaderProgram with the given OpenGL context and loads the default shader program.
        get_program(shader_program_name):
            Loads and compiles the vertex and fragment shaders from files and creates an OpenGL program.
            Args:
                shader_program_name (str): The name of the shader program to load.
            Returns:
                The compiled shader program.
        destroy():
            Releases all shader programs.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')

    def get_program(self, shader_program_name):
        """
        Loads and compiles a shader program from vertex and fragment shader files.
        Args:
            shader_program_name (str): The base name of the shader program files 
                                       (without extensions). The method expects 
                                       the files to be located in the 'shaders' 
                                       directory with '.vert' and '.frag' extensions.
        Returns:
            program: The compiled shader program object.
        """

        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    def destroy(self):
        """
        Releases all shader programs managed by this instance.
        This method iterates through all shader programs stored in the `programs` 
        dictionary and calls their `release` method to free up resources.
        """

        for program in self.programs.values():
            program.release()
