import glm
import pygame as pg

FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSIVITY = 0.05


class Camera:
    """
    A class to represent a camera in a 3D OpenGL graphic engine.
    Attributes
    ----------
    app : object
        The application instance.
    aspect_ratio : float
        The aspect ratio of the window.
    position : glm.vec3
        The position of the camera in 3D space.
    up : glm.vec3
        The up direction vector of the camera.
    right : glm.vec3
        The right direction vector of the camera.
    forward : glm.vec3
        The forward direction vector of the camera.
    yaw : float
        The yaw angle of the camera.
    pitch : float
        The pitch angle of the camera.
    m_view : glm.mat4
        The view matrix of the camera.
    m_proj : glm.mat4
        The projection matrix of the camera.
    Methods
    -------
    rotate():
        Rotates the camera based on mouse movement.
    update_camera_vectors():
        Updates the camera's direction vectors based on yaw and pitch.
    update():
        Updates the camera's position, rotation, and view matrix.
    move():
        Moves the camera based on keyboard input.
    get_view_matrix():
        Returns the view matrix of the camera.
    get_projection_matrix():
        Returns the projection matrix of the camera.
    """

    def __init__(self, app, position=(0, 0, 4), yaw=90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(2, 3, 3)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        # view matrix
        self.m_view = self.get_view_matrix()
        # projection matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        """
        Rotates the camera based on mouse movement.
        This method updates the camera's yaw and pitch angles according to the 
        relative movement of the mouse. The yaw is adjusted by the horizontal 
        movement, and the pitch is adjusted by the vertical movement. The pitch 
        is clamped to ensure it stays within a range of -90 to 89 degrees to 
        prevent flipping.
        Attributes:
            rel_x (int): The relative horizontal movement of the mouse.
            rel_y (int): The relative vertical movement of the mouse.
            SENSIVITY (float): A constant that determines how sensitive the 
                               rotation is to mouse movement.
        """

        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSIVITY
        self.pitch -= rel_y * SENSIVITY
        self.pitch = max(-90, min(89, self.pitch))

    def update_camera_vectors(self):
        """
        Updates the camera's direction vectors based on the current yaw and pitch angles.
        This method recalculates the forward, right, and up vectors of the camera using the 
        current yaw and pitch angles. The forward vector is computed using trigonometric 
        functions, and then normalized. The right vector is calculated as the cross product 
        of the forward vector and the world up vector (0, 1, 0), and then normalized. The up 
        vector is calculated as the cross product of the right and forward vectors, and then 
        normalized.
        This method should be called whenever the yaw or pitch angles are updated to ensure 
        the camera's direction vectors are correctly aligned.
        """

        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)
        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        """
        Updates the camera's position, orientation, and view matrix.
        This method performs the following steps:
        1. Moves the camera based on input or predefined logic.
        2. Rotates the camera based on input or predefined logic.
        3. Updates the camera's direction vectors (e.g., front, up, right).
        4. Recalculates the view matrix based on the updated position and orientation.
        """

        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        """
        Moves the camera based on keyboard input.
        The movement is determined by the keys pressed:
        - 'Z' key moves the camera forward.
        - 'S' key moves the camera backward.
        - 'Q' key moves the camera to the left.
        - 'D' key moves the camera to the right.
        - 'A' key moves the camera upward.
        - 'E' key moves the camera downward.
        The speed of the movement is scaled by the application's delta time to ensure consistent movement regardless of frame rate.
        """

        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_z]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_q]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_a]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        """
        Generates the view matrix for the camera.
        This method uses the camera's position, forward direction, and up vector
        to create a view matrix using the glm.lookAt function.
        Returns:
            glm.mat4: The view matrix representing the camera's perspective.
        """

        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        """
        Calculate and return the projection matrix for the camera.
        This method uses the perspective projection matrix formula from the glm library.
        Returns:
            glm.mat4: The perspective projection matrix.
        """

        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
