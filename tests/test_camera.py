import unittest
from unittest.mock import Mock, patch
import glm
import pygame as pg
from src.camera import Camera

# Define constants used in the Camera class
FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSIVITY = 0.05


class TestCamera(unittest.TestCase):
    def setUp(self):
        # Mock the application instance with required attributes
        self.mock_app = Mock()
        self.mock_app.WIN_SIZE = (800, 600)
        self.mock_app.delta_time = 1.0

        self.camera = Camera(self.mock_app)

    def test_initial_position(self):
        # Test if the initial position is set correctly
        self.assertEqual(self.camera.position, glm.vec3(2, 3, 3))

    def test_initial_view_matrix(self):
        # Test if the initial view matrix is created properly
        expected_view_matrix = glm.lookAt(
            self.camera.position, self.camera.position + self.camera.forward, self.camera.up)
        self.assertEqual(self.camera.m_view, expected_view_matrix)

    def test_initial_projection_matrix(self):
        # Test if the initial projection matrix is created properly
        expected_projection_matrix = glm.perspective(
            glm.radians(FOV), self.camera.aspect_ratio, NEAR, FAR)
        self.assertEqual(self.camera.m_proj, expected_projection_matrix)

    @patch('pygame.mouse.get_rel', return_value=(10, 5))
    def test_rotate(self, mock_get_rel):
        # Test rotation based on mouse movement
        initial_yaw = self.camera.yaw
        initial_pitch = self.camera.pitch

        # Call rotate to adjust yaw and pitch
        self.camera.rotate()

        # Check updated yaw and pitch
        expected_yaw = initial_yaw + 10 * SENSIVITY
        expected_pitch = initial_pitch - 5 * SENSIVITY
        self.assertEqual(self.camera.yaw, expected_yaw)
        self.assertEqual(self.camera.pitch, expected_pitch)

    def test_update_camera_vectors(self):
        # Test if the forward, right, and up vectors are updated correctly
        self.camera.yaw = 45
        self.camera.pitch = 30
        self.camera.update_camera_vectors()

        # Calculate expected forward vector based on yaw and pitch
        yaw_radians = glm.radians(self.camera.yaw)
        pitch_radians = glm.radians(self.camera.pitch)
        expected_forward = glm.vec3(
            glm.cos(yaw_radians) * glm.cos(pitch_radians),
            glm.sin(pitch_radians),
            glm.sin(yaw_radians) * glm.cos(pitch_radians)
        )
        expected_forward = glm.normalize(expected_forward)

        self.assertAlmostEqual(self.camera.forward.x,
                               expected_forward.x, places=5)
        self.assertAlmostEqual(self.camera.forward.y,
                               expected_forward.y, places=5)
        self.assertAlmostEqual(self.camera.forward.z,
                               expected_forward.z, places=5)

    @patch('pygame.key.get_pressed')
    def test_move_forward(self, mock_get_pressed):
        # Mock key press events for moving forward
        mock_get_pressed.return_value = {
            pg.K_z: True, pg.K_s: False, pg.K_q: False, pg.K_d: False, pg.K_a: False, pg.K_e: False}

        # Capture initial position and calculate expected new position
        initial_position = glm.vec3(self.camera.position)
        expected_position = initial_position + \
            (self.camera.forward * SPEED * self.mock_app.delta_time)

        self.camera.move()
        self.assertAlmostEqual(self.camera.position.x,
                               expected_position.x, places=5)
        self.assertAlmostEqual(self.camera.position.y,
                               expected_position.y, places=5)
        self.assertAlmostEqual(self.camera.position.z,
                               expected_position.z, places=5)

    def test_get_view_matrix(self):
        # Check if get_view_matrix returns the correct matrix
        view_matrix = self.camera.get_view_matrix()
        expected_matrix = glm.lookAt(
            self.camera.position, self.camera.position + self.camera.forward, self.camera.up)
        self.assertEqual(view_matrix, expected_matrix)

    def test_get_projection_matrix(self):
        # Check if get_projection_matrix returns the correct matrix
        projection_matrix = self.camera.get_projection_matrix()
        expected_matrix = glm.perspective(glm.radians(
            FOV), self.camera.aspect_ratio, NEAR, FAR)
        self.assertEqual(projection_matrix, expected_matrix)


if __name__ == '__main__':
    unittest.main()
