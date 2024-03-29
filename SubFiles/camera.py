from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians
import copy

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 4.0, 15.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])
        self.noclip = False
        self.mouse_sensitivity = 0.25
        self.jaw = -90
        self.pitch = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 90:
                self.pitch = 90
            if self.pitch < -90:
                self.pitch = -90

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))


        move = Vector3([0.0, 0.0, 0.0])
        move.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        move.z = sin(radians(self.jaw)) * cos(radians(self.pitch))


        self.camera_move = vector.normalise(move)
        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    # Camera method for the WASD movement
    def process_keyboard(self, direction, velocity, noclip):
        self.noclip = noclip
        future_pos = copy.deepcopy(self.camera_pos)
        if direction == "FORWARD":
            future_pos += self.camera_move * velocity
        if direction == "BACKWARD":
            future_pos -= self.camera_move * velocity
        if direction == "LEFT":
            future_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            future_pos += self.camera_right * velocity

        if not self.noclip:
            if 18.9 >= future_pos[0] >= -15 and 29.8 >= future_pos[2] >= -5.525:
                if direction == "FORWARD":
                    self.camera_pos += self.camera_move * velocity
                if direction == "BACKWARD":
                    self.camera_pos -= self.camera_move * velocity
                if direction == "LEFT":
                    self.camera_pos -= self.camera_right * velocity
                if direction == "RIGHT":
                    self.camera_pos += self.camera_right * velocity
        else:
            if direction == "FORWARD":
                self.camera_pos += self.camera_front * velocity *5
            if direction == "BACKWARD":
                self.camera_pos -= self.camera_front * velocity *5
            if direction == "LEFT":
                self.camera_pos -= self.camera_right * velocity *5
            if direction == "RIGHT":
                self.camera_pos += self.camera_right * velocity *5

