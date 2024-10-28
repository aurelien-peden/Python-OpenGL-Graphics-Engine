import numpy as np
import moderngl as mgl
import pywavefront


class VBO:
    """
    VBO class is responsible for managing Vertex Buffer Objects (VBOs) for different 3D models.
    Attributes:
        vbos (dict): A dictionary holding VBO instances for different models.
    Methods:
        __init__(ctx):
            Initializes the VBO class with a given context and creates VBOs for predefined models.
        destroy():
            Destroys all VBOs managed by this class to free up resources.
    """

    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['cat'] = CatVBO(ctx)

    def destroy(self):
        """
        Destroys all VBOs (Vertex Buffer Objects) managed by this instance.
        This method iterates through all VBOs stored in the `vbos` dictionary and calls their `destroy` method to release any resources they are using.
        """

        for vbo in self.vbos.values():
            vbo.destroy()

class BaseVBO:
    """
    BaseVBO is a base class for creating Vertex Buffer Objects (VBOs) in an OpenGL context.
    Attributes:
        ctx: The OpenGL context.
        vbo: The vertex buffer object created from vertex data.
        format (str): The format of the vertex data.
        attribs (list): The list of vertex attributes.
    Methods:
        __init__(ctx):
            Initializes the BaseVBO with the given OpenGL context.
        get_vertex_data():
            Abstract method to be implemented by subclasses to provide vertex data.
        get_vbo():
            Creates and returns a vertex buffer object from the vertex data.
        destroy():
            Releases the vertex buffer object.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self):
        pass

    def get_vbo(self):
        """
        Creates and returns a Vertex Buffer Object (VBO) containing vertex data.
        This method retrieves the vertex data using the `get_vertex_data` method,
        creates a buffer object using the context's buffer method, and returns
        the created VBO.
        Returns:
            vbo: The created Vertex Buffer Object containing the vertex data.
        """

        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        """
        Releases the Vertex Buffer Object (VBO) resources.
        This method should be called to properly clean up and release the 
        resources associated with the VBO when it is no longer needed.
        """

        self.vbo.release()


class CubeVBO(BaseVBO):
    """
    A class used to represent a Cube Vertex Buffer Object (VBO).
    Attributes
    ----------
    format : str
        The format of the VBO, specifying the layout of the vertex attributes.
    attribs : list
        A list of attribute names corresponding to the vertex attributes.
    Methods
    -------
    get_data(vertices, indices)
        Static method that flattens the vertex data based on the provided indices.
    get_vertex_data()
        Generates and returns the vertex data for the cube, including texture coordinates and normals.
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        """
        Generates a flattened array of vertex data based on provided indices.
        Args:
            vertices (list or np.ndarray): A list or array of vertex data.
            indices (list of lists): A list of lists where each sublist contains indices that form a triangle.
        Returns:
            np.ndarray: A flattened array of vertex data corresponding to the provided indices, with dtype 'f4'.
        """

        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')
    
    def get_vertex_data(self):
        """
        Generates and returns the vertex data for a 3D object, including vertex positions, 
        texture coordinates, and normals.
        Returns:
            np.ndarray: A numpy array containing the combined vertex data, texture coordinates, 
                        and normals for the 3D object.
        """

        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data
    
class CatVBO(BaseVBO):
    """
    A class used to represent a Vertex Buffer Object (VBO) for a cat model.
    Attributes
    ----------
    format : str
        The format of the vertex data.
    attribs : list
        The list of attribute names for the vertex data.
    Methods
    -------
    get_vertex_data():
        Loads and returns the vertex data from the cat model file.
    """

    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        """
        Loads vertex data from a Wavefront OBJ file and returns it as a NumPy array.
        This method uses the pywavefront library to load an OBJ file located at 
        'objects/cat/12221_Cat_v1_l3.obj'. It extracts the vertex data from the 
        first material in the loaded Wavefront object and converts it into a 
        NumPy array with a data type of float32 ('f4').
        Returns:
            numpy.ndarray: A NumPy array containing the vertex data from the OBJ file.
        """

        objs = pywavefront.Wavefront('objects/cat/12221_Cat_v1_l3.obj')
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data