from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from SubFiles import shaders
import pygame
import pyrr
from SubFiles import objectLoader
from SubFiles.textureLoader import load_textures
from SubFiles.camera import Camera


class graphic():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.first_mouse = True
        self.models = []
        self.models_boolean = []
        self.object_locations = []
        self.models_offset = [0, 0, 0, 0]
        self.object_counter = 0
        self.mouse_counter = 0

        self.compile_shader()
        self.create_object()
        self.generate_custom_colour()
        self.initialise_camera()
        self.initalise_buffers()
        self.projection()


    def initialise_camera(self):
        self.cam = Camera()
        self.lastX, self.lastY = self.width / 2, self.height / 2
        self.first_mouse = True

    def textures(self):

        self.texture = glGenTextures(4)

    def projection(self):
        # Use shader
        glUseProgram(self.shader)

        # Create background colour
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Perpective projection
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.width / self.height, 0.1, 100)

        # Pick_colours
        self.pick_colours = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 0, 0)]

        # Get locations
        self.model_location = glGetUniformLocation(self.shader, "model")
        self.projection_location = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.icolor_loc = glGetUniformLocation(self.shader, "icolor")
        self.switcher_loc = glGetUniformLocation(self.shader, "switcher")

        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)

    def display(self):

        glClearColor(0, 0.2, 0.1, 1)

        # Fill background colours
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Specify Colour or Texture
        glUniform1i(self.switcher_loc, 0)

        # Draw
        for i in range(len(self.models)):

            glBindVertexArray(self.VAO[i])
            glBindTexture(GL_TEXTURE_2D, self.texture[i])

            if self.models_boolean[i]:
                self.models_offset[i] += self.x_offset * -1
                """Rotation
                self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, rotation @ self.object_locations[i])"""

                #Translation
                self.rotation = pyrr.Matrix44.from_translation((self.x_offset/20, 0,0))
                self.object_locations[i] = self.rotation @ self.object_locations[i]

                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])

            else:
                """Rotation
                self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])"""

                #Translation
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])

            glDrawArrays(GL_TRIANGLES, 0, len(self.models[i][0]))

        # Picker frame buffer
        glUniform1i(self.switcher_loc, 1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw
        for i in range(len(self.models)):

            glBindVertexArray(self.VAO[i])
            glUniform3iv(self.icolor_loc, 1, self.pick_colours[i])

            if self.models_boolean[i]:
                """Rotation:
                self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])"""

                #Translation:
                self.rotation = pyrr.Matrix44.from_translation((self.x_offset / 20, 0, 0))

                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])
            else:
                """Rotation:
                self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])
                """
                # Translation
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])
            glDrawArrays(GL_TRIANGLES, 0, len(self.models[i][0]))

    def compile_shader(self):
        # Compile shaders

        self.shader = compileProgram(compileShader(shaders.vertex_src, GL_VERTEX_SHADER),
                                     compileShader(shaders.fragment_src, GL_FRAGMENT_SHADER))

    def initalise_buffers(self):
        # Vertex Array Object
        self.VAO = glGenVertexArrays(len(self.models))
        VBO = glGenBuffers(len(self.models))

        for i in range(0, len(self.models)):
            glBindVertexArray(self.VAO[i])

            glBindBuffer(GL_ARRAY_BUFFER, VBO[i])
            glBufferData(GL_ARRAY_BUFFER, self.models[i][1].nbytes, self.models[i][1], GL_STATIC_DRAW)

            # Layer 1 (Position)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.models[i][1].itemsize * 8, ctypes.c_void_p(0))

            # Layer 2 (Texture)
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.models[i][1].itemsize * 8, ctypes.c_void_p(12))

    def window_resize(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.width / self.height, 0.1, 100)
        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)

    def player_move(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.cam.process_keyboard("FORWARD", 1)
        if keys_pressed[pygame.K_a]:
            self.cam.process_keyboard("LEFT", 1)
        if keys_pressed[pygame.K_s]:
            self.cam.process_keyboard("BACKWARD", 1)
        if keys_pressed[pygame.K_d]:
            self.cam.process_keyboard("RIGHT", 1)

        # Move camera
        self.view = self.cam.get_view_matrix()

        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view)

    def mouse_move(self):



        mouse_pos = pygame.mouse.get_pos()



        self.mouse_look(mouse_pos[0], mouse_pos[1])

    def mouse_look(self, x, y):
        pygame.mouse.set_pos(self.width / 2, self.height / 2 )

        if self.first_mouse:
            self.mouse_counter += 1
            self.cam.process_mouse_movement(0, 0)

            self.x_offset = 0
            self.y_offset = 0

        else:
            self.x_offset = x - self.width / 2
            self.y_offset = self.height / 2 - y

            self.cam.process_mouse_movement(self.x_offset, self.y_offset)

        if self.mouse_counter >= 3:
            self.first_mouse = False



    def make_object(self, object_path, texture_path, position):
        self.models.append(objectLoader.ObjLoader.load_model(object_path))
        load_textures(texture_path, self.texture[self.object_counter])
        self.object_counter += 1
        self.object_locations.append(pyrr.matrix44.create_from_translation(pyrr.Vector3(position)))

    def create_object(self):
        self.textures()

        self.make_object("Objects/floor.obj", "Textures/Brick_Block.png", [0, 0, 0])
        self.make_object("Objects/dragonlore.obj", "Textures/dragon_lore.bmp", [-6, 10, 0])
        self.make_object("Objects/teapot.obj", "Textures/blue.jpg", [0, 0, 0])
        self.make_object("Objects/TreasureBox.obj", "Textures/wooden_box.jpg", [10, 1, 0])

        for i in range(4):
            self.models_boolean.append(False)
            self.models_offset[i] = 0

    def generate_custom_colour(self):
        # picking texture and a frame buffer object
        pick_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, pick_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 1280, 720, 0, GL_RGB, GL_FLOAT, None)

        self.FBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, pick_texture, 0)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def pick(self, mouse_x, mouse_y):
        colour = glReadPixels(mouse_x, mouse_y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        if colour[0] == 255:
            print("red")
            self.models_boolean[0] = not self.models_boolean[0]
        elif colour[1] == 255:
            print("blue")
            self.models_boolean[1] = not self.models_boolean[1]
        elif colour[2] == 255:
            print("green")
            self.models_boolean[2] = not self.models_boolean[2]
        elif colour[2] == 0:
            self.models_boolean[3] = not self.models_boolean[3]

    def change_dimensions(self, width, height):
        self.width = width
        self.height = height

    def get_state (self):
        return self.object_locations, self.models_offset
