import unittest
import glm
from src.light import Light


class TestLight(unittest.TestCase):

    def test_initial_position(self):
        # Test default position initialization
        light = Light()
        expected_position = glm.vec3(3, 3, -3)
        self.assertEqual(light.position, expected_position)

        # Test custom position initialization
        custom_position = (10, 5, -7)
        light = Light(position=custom_position)
        self.assertEqual(light.position, glm.vec3(custom_position))

    def test_initial_color(self):
        # Test default color initialization
        light = Light()
        expected_color = glm.vec3(1, 1, 1)
        self.assertEqual(light.color, expected_color)

        # Test custom color initialization
        custom_color = (0.5, 0.5, 0.5)
        light = Light(color=custom_color)
        self.assertEqual(light.color, glm.vec3(custom_color))

    def test_ambient_intensity(self):
        # Test that ambient intensity (Ia) is 10% of the color
        color = (1, 1, 1)
        light = Light(color=color)
        expected_Ia = glm.vec3(color) * 0.1
        self.assertEqual(light.Ia, expected_Ia)

        # Test ambient intensity for a custom color
        color = (0.2, 0.3, 0.4)
        light = Light(color=color)
        expected_Ia = glm.vec3(color) * 0.1
        self.assertEqual(light.Ia, expected_Ia)

    def test_diffuse_intensity(self):
        # Test that diffuse intensity (Id) is 80% of the color
        color = (1, 1, 1)
        light = Light(color=color)
        expected_Id = glm.vec3(color) * 0.8
        self.assertEqual(light.Id, expected_Id)

        # Test diffuse intensity for a custom color
        color = (0.3, 0.6, 0.9)
        light = Light(color=color)
        expected_Id = glm.vec3(color) * 0.8
        self.assertEqual(light.Id, expected_Id)

    def test_specular_intensity(self):
        # Test that specular intensity (Is) is 100% of the color
        color = (1, 1, 1)
        light = Light(color=color)
        expected_Is = glm.vec3(color) * 1.0
        self.assertEqual(light.Is, expected_Is)

        # Test specular intensity for a custom color
        color = (0.4, 0.7, 0.1)
        light = Light(color=color)
        expected_Is = glm.vec3(color) * 1.0
        self.assertEqual(light.Is, expected_Is)


if __name__ == '__main__':
    unittest.main()
