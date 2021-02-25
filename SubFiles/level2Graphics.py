from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from SubFiles import shaders
import pygame
import pyrr
from SubFiles import objectLoader
from SubFiles.textureLoader import load_textures
from SubFiles.camera import Camera


class graphic():

    def __init__(self, width, height, choice):
        self.width = width
        self.height = height
        self.first_mouse = True
        self.models = []
        self.inventory_models = []
        self.inventory_choice = choice
        self.models_boolean = []
        self.object_locations = []
        self.models_offset = []
        self.models_maxoffset = [-10, -50, 0, -50, -50, 0, 0,125, 30]
        self.object_counter = 0
        self.mouse_counter = 0
        self.inventory = [0, 0, 0]
        self.game_finished = False
        self.key_inserted = False
        self.pick_boolean = [True, False, False, False, False, False, False, False, False, False]
        self.equip_sound = pygame.mixer.Sound("Audio/equip.mp3")
        self.unlock_sound = pygame.mixer.Sound("Audio/unlock.mp3")
        self.gamecomplete_sound = pygame.mixer.Sound("Audio/GameComplete.mp3")

        # Boot up the graphic procedures
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
        self.pick_colours = [(255, 0, 0), (244, 0, 0), (233, 0, 0), (222, 0, 0), (211, 0, 0), (200, 0, 0),(0,0,0), (199,0,0), (188,0,0)]

        # Get locations
        self.model_location = glGetUniformLocation(self.shader, "model")
        self.projection_location = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.icolor_loc = glGetUniformLocation(self.shader, "icolor")
        self.switcher_loc = glGetUniformLocation(self.shader, "switcher")
        # self.light_loc = glGetUniformLocation(self.shader, "light")

        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)

    def display(self):

        glClearColor(0, 0.2, 0.1, 1)

        # Fill background colours
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Specify Colour or Texture
        glUniform1i(self.switcher_loc, 0)

        # Draw
        for i in range(len(self.models)):

            if i == 6 and not self.key_inserted:
                continue
            glBindVertexArray(self.VAO[i])
            glBindTexture(GL_TEXTURE_2D, self.texture[i])

            if self.models_boolean[i]:

                """
                Translation
                if self.models_maxoffset[i] > -100:
                    self.models_maxoffset[i] += self.x_offset * -1
                    self.models_offset[i] += self.x_offset * -1
                    # Translation
                    self.rotation = pyrr.Matrix44.from_translation((self.x_offset / 20, 0, 0))
                    self.object_locations[i] = self.rotation @ self.object_locations[i]

                    print(self.models_maxoffset[i])"""

                """Rotation
                self.models_offset[i] += self.y_offset * -1
                self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, rotation @ self.object_locations[i])"""
                # Slide horizontal bar
                if i == 0:
                    if self.x_offset <= 0:
                        if self.models_offset[i] >= self.models_maxoffset[i]:

                            if self.x_offset >= -4:
                                self.models_offset[i] += self.x_offset
                                self.rotation = pyrr.Matrix44.from_y_rotation(self.x_offset / 700)
                                self.object_locations[i] = self.object_locations[i] @ self.rotation
                        else:
                            self.models_boolean[i] = False
                            self.pick_boolean[i] = False
                            self.pick_boolean[1] = True
                # Slide key slot
                elif i == 1:
                    if self.y_offset <= 0:
                        if self.models_offset[i] >= self.models_maxoffset[i]:
                            if self.y_offset >= -4:
                                self.models_offset[i] += self.y_offset
                                self.rotation = pyrr.Matrix44.from_translation((0, 0, self.y_offset  / 100))

                                # Move key as well
                                self.object_locations[2] = self.object_locations[2] @ self.rotation
                                self.object_locations[i] = self.object_locations[i] @ self.rotation
                        else:
                            self.pick_boolean[i] = False
                            self.models_boolean[i] = False
                            self.pick_boolean[2] = True
                            self.pick_boolean[3] = True
                # Key clicked
                elif i == 2:
                    self.models[i] = (None, None)
                    self.models_boolean[i] = False
                # Middle box moved
                elif i == 3:
                    if self.y_offset <= 0:
                        if self.models_offset[i] >= self.models_maxoffset[i]:
                            if self.y_offset >= -4:
                                self.models_offset[i] += self.y_offset
                                self.rotation = pyrr.Matrix44.from_translation((0, 0, self.y_offset  / 100))

                                # Move upper box, key slide as well
                                self.object_locations[4] = self.object_locations[4] @ self.rotation
                                self.object_locations[5] = self.object_locations[5] @ self.rotation
                                self.object_locations[7] = self.object_locations[7] @ self.rotation
                                self.object_locations[6] = self.object_locations[6] @ self.rotation
                                self.object_locations[i] = self.object_locations[i] @ self.rotation
                        else:
                            self.pick_boolean[i] = False
                            self.models_boolean[i] = False
                            self.pick_boolean[4] = True

                # Move key slot
                elif i == 4:
                    if self.y_offset <= 0:
                        if self.models_offset[i] >= self.models_maxoffset[i]:
                            if self.y_offset >= -4:
                                self.models_offset[i] += self.y_offset
                                self.rotation = pyrr.Matrix44.from_translation((0,  self.y_offset  / 100, 0))


                                self.object_locations[i] = self.object_locations[i] @ self.rotation
                        else:
                            self.pick_boolean[i] = False
                            self.models_boolean[i] = False
                            self.pick_boolean[5] = True

                # Move upper box
                elif i == 7:
                    if self.x_offset >= 0:
                        if self.models_offset[i] <= self.models_maxoffset[i]:
                            if self.x_offset <= 4:

                                self.models_offset[i] += self.x_offset
                                self.rotation = pyrr.Matrix44.from_translation((self.x_offset * -1 / 50, 0  , 0))
                                self.object_locations[i] = self.object_locations[i] @ self.rotation
                        else:
                            self.pick_boolean[i] = False
                            self.models_boolean[i] = False
                            self.pick_boolean[8] = True

                # Move book
                elif i == 8:
                    if self.y_offset >= 0:
                        if self.models_offset[i] <= self.models_maxoffset[i]:
                            if self.y_offset <= 4:
                                self.models_offset[i] += self.y_offset * 1
                                self.rotation = pyrr.Matrix44.from_x_rotation(self.y_offset  / 700)
                                self.object_locations[i] = self.object_locations[i] @ self.rotation
                        else:
                            self.models_boolean[i] = False




                if self.models[i][0] is not None:
                    glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])
                # glUniformMatrix4fv(self.light_loc, 1, GL_FALSE, self.object_locations[i])

            else:
                """Rotation
                self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])"""

                # Translation
                if self.models[i][0] is not None:
                    glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])
                # glUniformMatrix4fv(self.light_loc, 1, GL_FALSE, self.object_locations[i])
            if self.models[i][0] is not None:
                glDrawArrays(GL_TRIANGLES, 0, len(self.models[i][0]))

        # Picker frame buffer
        glUniform1i(self.switcher_loc, 1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Draw
        for i in range(len(self.pick_colours)):
            if self.pick_boolean[i]:
                glBindVertexArray(self.VAO[i])
                glUniform3iv(self.icolor_loc, 1, self.pick_colours[i])

                if self.models_boolean[i]:
                    """Rotation:
                    self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                    glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])"""

                    # Translation:

                    if self.models[i][0] is not None:
                        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])


                else:
                    """Rotation:
                    self.rotation = pyrr.Matrix44.from_y_rotation(self.models_offset[i] / 25)
                    glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.rotation @ self.object_locations[i])
                    """
                    # Translation
                    if self.models[i][0] is not None:
                        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.object_locations[i])
                if self.models[i][0] is not None:
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

            # Layer 3 (Normal)

            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.models[i][1].itemsize * 8, ctypes.c_void_p(20))
            glEnableVertexAttribArray(2)

    def window_resize(self, width, height):
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.width / self.height, 0.1, 100)
        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)

    def player_move(self, keys_pressed):
        self.keys_pressed = keys_pressed
        if keys_pressed[pygame.K_w]:
            self.cam.process_keyboard("FORWARD", 0.2)
        if keys_pressed[pygame.K_a]:
            self.cam.process_keyboard("LEFT", 0.2)
        if keys_pressed[pygame.K_s]:
            self.cam.process_keyboard("BACKWARD", 0.2)
        if keys_pressed[pygame.K_d]:
            self.cam.process_keyboard("RIGHT", 0.2)

        # Move camera

        self.view = self.cam.get_view_matrix()
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view)

    def mouse_move(self):

        mouse_pos = pygame.mouse.get_pos()

        self.mouse_look(mouse_pos[0], mouse_pos[1])

    def mouse_look(self, x, y):
        pygame.mouse.set_pos(self.width / 2, self.height / 2)

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
        self.texture = glGenTextures(13)

        self.make_object("Objects/horizontal_slide.obj", "Textures/rosewood.jpg", [11, -25, 35])
        self.make_object("Objects/key_slot.obj", "Textures/rosewood.jpg", [11, -25, 35])
        self.make_object("Objects/key.obj", "Textures/flap.jpg", [11, -25, 35])
        self.make_object("Objects/middle_puzzle.obj", "Textures/rosewood.jpg", [11, -25, 35])
        self.make_object("Objects/key_slide.obj", "Textures/rosewood.jpg", [11, -25, 35])
        self.make_object("Objects/key_plane.obj", "Textures/wallpaper.jpg", [11, -25, 35])
        self.make_object("Objects/inserted_key.obj", "Textures/flap.jpg", [11, -25, 35])
        self.make_object("Objects/upper_puzzle.obj", "Textures/rosewood.jpg", [11, -25, 35])
        self.make_object("Objects/book.obj", "Textures/book.jpg", [11, -25, 35])
        self.make_object("Objects/Room.obj", "Textures/table.jpg", [0, 8, 50])
        self.make_object("Objects/floor.obj", "Textures/Brick_Block.png", [2, -1, 10])
        self.make_object("Objects/Table.obj", "Textures/wallpaper.jpg", [11, -25, 35])
        self.make_object("Objects/bottom_puzzle.obj", "Textures/rosewood.jpg", [11, -25, 35])



        for i in range(13):
            self.models_boolean.append(False)
            self.models_offset.append(0)

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

        # If clicked on horizontal slide
        if colour[0] == 255:
            self.models_boolean[0] = not self.models_boolean[0]

        # If click on key slot:
        elif colour[0] == 244:
            self.models_boolean[1] = not self.models_boolean[1]

        # If key is clicked:
        elif colour[0] == 233:
            self.inventory[1] = 2
            self.models_boolean[2] = not self.models_boolean[2]
            self.equip_sound.play()
        # If middle box is moved
        elif colour[0] == 222:
            if self.inventory[self.inventory_choice] == 0:
                self.models_boolean[3] = not self.models_boolean[3]
        # If the slide is being moved
        elif colour[0] == 211:
            if self.inventory[self.inventory_choice] == 0:
                self.models_boolean[4] = not self.models_boolean[4]
        # If the keyhole is clicked
        elif colour[0] == 200:
            if self.inventory[self.inventory_choice] == 2:
                # Move key to the keyhole
                self.key_inserted = True
                self.pick_boolean[5] = False
                self.inventory[self.inventory_choice] = 0
                self.pick_boolean[7] = True
                self.unlock_sound.play()

        # If the upper box is clicked
        elif colour[0] == 199:
            self.models_boolean[7] = not self.models_boolean[7]

        # If book is clicked
        elif colour[0] == 188:
            if self.models_offset[8] < 30:
                if self.inventory[self.inventory_choice] == 0:
                    self.models_boolean[8] = not self.models_boolean[8]
            else:
                self.game_finished = True
                self.gamecomplete_sound.play()



    def checkwin(self):
        return self.game_finished

    def change_dimensions(self, width, height):
        self.width = width
        self.height = height

    def get_state(self):
        return self.object_locations, self.models_offset, self.models_maxoffset, self.models, self.cam.camera_pos, \
               self.cam.camera_up, self.cam.camera_front, self.cam.camera_right, self.cam.jaw, self.cam.pitch, self.inventory, \
               self.pick_boolean, self.key_inserted
