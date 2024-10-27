import glm

class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        # Intensities
        self.Ia = self.color * 0.1 # ambient intensity
        self.Id = self.color * 0.8 # diffuse intensity
        self.Is = self.color * 1.0 # specular intensity