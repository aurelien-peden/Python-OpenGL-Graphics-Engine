import pygame as pg
import moderngl as mgl


class Texture:
    """
    A class to manage textures in an OpenGL context using Pygame.
    Attributes
    ----------
    ctx : moderngl.Context
        The OpenGL context.
    textures : dict
        A dictionary to store loaded textures.
    Methods
    -------
    __init__(ctx)
        Initializes the Texture object with the given OpenGL context and loads predefined textures.
    get_texture(path)
        Loads a texture from the given file path, flips it vertically, and creates an OpenGL texture object.
    destroy()
        Releases all loaded textures.
    """

    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}
        self.textures[0] = self.get_texture('textures/img.jpg')
        self.textures[1] = self.get_texture('textures/img_1.jpg')
        self.textures[2] = self.get_texture('textures/img_2.jpg')
        self.textures[3] = self.get_texture('objects/cat/cat_diffuse.jpg')

    def get_texture(self, path):
        """
        Loads a texture from the given file path, processes it, and returns the texture object.
        Args:
            path (str): The file path to the texture image.
        Returns:
            mgl.Texture: The processed texture object.
        The function performs the following steps:
        1. Loads the texture image from the specified path using pygame.
        2. Flips the image vertically to correct the y-axis orientation.
        3. Converts the image to a ModernGL texture object with 3 color components (RGB).
        4. Sets the texture filtering to use linear mipmap linear filtering.
        5. Builds mipmaps for the texture.
        6. Sets the anisotropy level to 32.0 for improved texture quality at oblique viewing angles.
        """

        texture = pg.image.load(path).convert()
        # flip image vertically because the y-axis is inverted in pygame
        texture = pg.transform.flip(texture, False, True)
        texture = self.ctx.texture(size=texture.get_size(
        ), components=3, data=pg.image.tostring(texture, 'RGB'))

        # mimaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        """
        Releases all textures managed by this instance.
        This method iterates over all textures stored in the `textures` dictionary
        and calls their `release` method to free up resources.
        """

        for texture in self.textures.values():
            texture.release()
