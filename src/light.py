import glm


class Light:
    """
    Light class represents a light source in a 3D scene.
    Attributes:
        position (glm.vec3): The position of the light source in 3D space.
        color (glm.vec3): The color of the light source.
        Ia (glm.vec3): Ambient intensity of the light.
        Id (glm.vec3): Diffuse intensity of the light.
        Is (glm.vec3): Specular intensity of the light.
    Methods:
        __init__(position, color): Initializes the Light object with a position and color.
    """

    def __init__(self, position=(3, 3, -3), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        # Intensities
        self.Ia = self.color * 0.1  # ambient intensity
        self.Id = self.color * 0.8  # diffuse intensity
        self.Is = self.color * 1.0  # specular intensity
