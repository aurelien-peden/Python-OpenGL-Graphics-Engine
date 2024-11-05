import unittest
from unittest.mock import Mock, patch
from src.mesh import Mesh


class TestMesh(unittest.TestCase):

    def setUp(self):
        # Mock the application context and VAO/Texture classes
        self.mock_app = Mock()
        self.mock_app.ctx = Mock()

    @patch('src.mesh.VAO')
    @patch('src.mesh.Texture')
    def test_initialization(self, MockTexture, MockVAO):
        # Create instance of Mesh with mocks
        mesh = Mesh(self.mock_app)

        # Check if VAO and Texture are initialized with app context
        MockVAO.assert_called_once_with(self.mock_app.ctx)
        MockTexture.assert_called_once_with(self.mock_app.ctx)

        # Verify that mesh.vao and mesh.texture are the specific mocked instances
        self.assertEqual(mesh.vao, MockVAO.return_value)
        self.assertEqual(mesh.texture, MockTexture.return_value)

    @patch('src.mesh.VAO')
    @patch('src.mesh.Texture')
    def test_destroy(self, MockTexture, MockVAO):
        # Mock the destroy methods for VAO and Texture
        mock_vao = Mock()
        mock_texture = Mock()
        MockVAO.return_value = mock_vao
        MockTexture.return_value = mock_texture

        # Create instance of Mesh with mocks
        mesh = Mesh(self.mock_app)

        # Call the destroy method
        mesh.destroy()

        # Check if destroy was called on VAO and Texture
        mock_vao.destroy.assert_called_once()
        mock_texture.destroy.assert_called_once()


if __name__ == '__main__':
    unittest.main()
