from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import shaders
import pygame
import pyrr
import numpy
import objectLoader
from textureLoader import load_textures
from SubFiles.camera import Camera


class graphic():

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.first_mouse = True
        self.object_counter = 0

        self.load_objects()
        self.compile_shader()
        self.initialise_camera()
        self.initialise_buffers()

        #self.initialise_instanced_buffer()
        self.textures()
        #self.instanced_textures()
        #self.instance()
        self.projection()

    def initialise_camera(self):
        self.cam = Camera()
        self.lastX, self.lastY = self.width / 2, self.height / 2
        self.first_mouse = True

    def textures(self):
        self.texture = glGenTextures(4)

        # To do len of directory

        load_textures("textures/wooden_box.png", self.texture[0])
        load_textures("../Textures/blue.jpg", self.texture[1])
        load_textures("../Textures/Brick_Block.png", self.texture[2])
        load_textures("../Textures/dragon_lore.bmp", self.texture[3])

    def projection(self):
        # Use shader
        glUseProgram(self.shader)

        # Create background colour

        glClearColor(0, 0.2, 0.1, 1)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Matrixes

        # Perpective projection
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, self.width / self.height, 0.1, 100)

        # Translates the object further away
        self.cube1 = pyrr.matrix44.create_from_translation(pyrr.Vector3([6, 1, 0]))
        self.teapot = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
        self.dragonlore = pyrr.matrix44.create_from_translation(pyrr.Vector3([-6, 10, 0]))
        self.floor = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))


        # Get locations
        self.model_location = glGetUniformLocation(self.shader, "model")
        self.projection_location = glGetUniformLocation(self.shader, "projection")
        self.view_loc = glGetUniformLocation(self.shader, "view")
        self.switcher_loc = glGetUniformLocation(self.shader, "switcher")

        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)

    def display(self):
        # Specify Colour or Texture
        glUniform1i(self.switcher_loc, 0)

        # draw the cube
        glBindVertexArray(self.VAO[0])
        glBindTexture(GL_TEXTURE_2D, self.texture[0])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.cube1)
        glDrawArrays(GL_TRIANGLES, 0, len(self.cube_indicies))

        # draw the teapot
        glBindVertexArray(self.VAO[1])
        glBindTexture(GL_TEXTURE_2D, self.texture[1])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.teapot)
        glDrawArrays(GL_TRIANGLES, 0, len(self.teapot_indicies))

        # draw the floor
        glBindVertexArray(self.VAO[2])
        glBindTexture(GL_TEXTURE_2D, self.texture[2])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.floor)
        glDrawArrays(GL_TRIANGLES, 0, len(self.floor_indicies))

        # draw the gun
        glBindVertexArray(self.VAO[3])
        glBindTexture(GL_TEXTURE_2D, self.texture[3])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.dragonlore)
        glDrawArrays(GL_TRIANGLES, 0, len(self.lore_indicies))





    def compile_shader(self):
        # Compile shaders

        self.shader = compileProgram(compileShader(shaders.vertex_src, GL_VERTEX_SHADER),
                                     compileShader(shaders.fragment_src, GL_FRAGMENT_SHADER))

    def initialise_buffers(self):
        # Buffer

        # Vertex Array Object
        self.VAO = glGenVertexArrays(4)
        VBO = glGenBuffers(4)

        # Cube

        # Vertex Buffer Object (Vertices)
        glBindVertexArray(self.VAO[0])

        glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
        glBufferData(GL_ARRAY_BUFFER, self.cube_buffer.nbytes, self.cube_buffer, GL_STATIC_DRAW)

        # Layer 1 (Position)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.cube_buffer.itemsize * 8, ctypes.c_void_p(0))

        # Layer 2 (Texture)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.cube_buffer.itemsize * 8, ctypes.c_void_p(12))

        # Layer 3 (Colour)
        # glEnableVertexAttribArray(2)
        # glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, drawing.vertices.itemsize * 8, ctypes.c_void_p(24))

        # Teapot

        glBindVertexArray(self.VAO[1])

        glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
        glBufferData(GL_ARRAY_BUFFER, self.teapot_buffer.nbytes, self.teapot_buffer, GL_STATIC_DRAW)

        # teapot vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.teapot_buffer.itemsize * 8, ctypes.c_void_p(0))

        # teapot textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.teapot_buffer.itemsize * 8, ctypes.c_void_p(12))

        # teapot normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.floor_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Floor
        glBindVertexArray(self.VAO[2])
        glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
        glBufferData(GL_ARRAY_BUFFER, self.floor_buffer.nbytes, self.floor_buffer, GL_STATIC_DRAW)

        # floor vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.floor_buffer.itemsize * 8, ctypes.c_void_p(0))
        # floor textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.floor_buffer.itemsize * 8, ctypes.c_void_p(12))
        # floor normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.floor_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # Gun
        glBindVertexArray(self.VAO[3])

        glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
        glBufferData(GL_ARRAY_BUFFER, self.lore_buffer.nbytes, self.lore_buffer, GL_STATIC_DRAW)

        # teapot vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.lore_buffer.itemsize * 8, ctypes.c_void_p(0))

        # teapot textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.lore_buffer.itemsize * 8, ctypes.c_void_p(12))

        # teapot normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.lore_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)





    def rotaion(self):
        # Clock
        ct = pygame.time.get_ticks() / 1000

        # Specify Colour or Texture
        glUniform1i(self.switcher_loc, 0)

        # Rotation
        rot_x = pyrr.Matrix44.from_y_rotation(0.4 * ct)
        rot_y = pyrr.Matrix44.from_x_rotation(0.8 * ct)
        rotation = pyrr.matrix44.multiply(rot_y, rot_x)

        # box
        glBindVertexArray(self.VAO[0])
        glBindTexture(GL_TEXTURE_2D, self.texture[0])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.cube1)
        glDrawArrays(GL_TRIANGLES, 0, len(self.cube_indicies))

        # Rotate teapot
        glBindVertexArray(self.VAO[1])
        model = pyrr.matrix44.multiply(rot_x, self.teapot)
        glBindTexture(GL_TEXTURE_2D, self.texture[1])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, model)
        glDrawArrays(GL_TRIANGLES, 0, len(self.teapot_indicies))

        # draw the floor
        glBindVertexArray(self.VAO[2])
        glBindTexture(GL_TEXTURE_2D, self.texture[2])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.floor)
        glDrawArrays(GL_TRIANGLES, 0, len(self.floor_indicies))

        # draw the gun
        glBindVertexArray(self.VAO[3])
        glBindTexture(GL_TEXTURE_2D, self.texture[3])
        glUniformMatrix4fv(self.model_location, 1, GL_FALSE, self.dragonlore)
        glDrawArrays(GL_TRIANGLES, 0, len(self.lore_indicies))

    def window_resize(self, width, height):
        glViewport(0, 0, width, height)
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, width / height, 0.1, 100)
        glUniformMatrix4fv(self.projection_location, 1, GL_FALSE, projection)

    def load_objects(self):

        self.teapot_indicies, self.teapot_buffer = objectLoader.ObjLoader.load_model("../Objects/teapot.obj")
        self.floor_indicies, self.floor_buffer = objectLoader.ObjLoader.load_model("../Objects/floor.obj")
        self.cube_indicies, self.cube_buffer = objectLoader.ObjLoader.load_model("Objects/cube.obj")
        self.lore_indicies, self.lore_buffer = objectLoader.ObjLoader.load_model("../Objects/dragonlore.obj")


    def player_move(self, keys_pressed):
        if keys_pressed[pygame.K_w]:
            self.cam.process_keyboard("FORWARD", 1)
        if keys_pressed[pygame.K_a]:
            self.cam.process_keyboard("LEFT", 1)
        if keys_pressed[pygame.K_s]:
            self.cam.process_keyboard("BACKWARD", 1)
        if keys_pressed[pygame.K_d]:
            self.cam.process_keyboard("RIGHT", 1)

        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] <= 0:
            pygame.mouse.set_pos((self.width - 1, mouse_pos[1]))
            self.lastX = self.width - 2

        elif mouse_pos[0] >= self.width - 1:
            pygame.mouse.set_pos((1, mouse_pos[1]))
            self.lastX = 1
        else:
            self.mouse_look(mouse_pos[0], mouse_pos[1])

        # Fill background colours
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Move camera
        self.view = self.cam.get_view_matrix()

        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, self.view)

    def mouse_look(self, x, y):

        pygame.mouse.set_pos(self.width / 2, self.height / 2)

        self.lastX = self.width / 2
        self.lastY = self.height / 2

        x_offset = x - self.lastX
        y_offset = self.lastY - y

        self.lastX = x
        self.lastY = y

        if self.first_mouse:
            self.cam.process_mouse_movement(0, 0)
            self.first_mouse = False
        else:
            self.cam.process_mouse_movement(x_offset, y_offset)

    def instance(self):
        # instance VBO
        instance_array = []
        offset = 1
        for z in range(0, 70, 10):
            for y in range(0,70, 10):
                for x in range(0, 70, 10):
                    translation = pyrr.Vector3([0.0, 0.0, 0.0])
                    translation.x = x + offset
                    translation.y = y + offset
                    translation.z = z + offset
                    instance_array.append(translation)

        self.len_of_instance_array = len(instance_array)  # do this before you flatten the array
        instance_array = numpy.array(instance_array, numpy.float32).flatten()

        instanceVBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, instanceVBO)
        glBufferData(GL_ARRAY_BUFFER, instance_array.nbytes, instance_array, GL_STATIC_DRAW)

        glEnableVertexAttribArray(3)
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))
        glVertexAttribDivisor(3, 1)  # 1 means, every instance will have it's own translation

    def initialise_instanced_buffer(self):

        # Vertex Array Object
        self.VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)

        # Teapot

        glBindVertexArray(self.VAO )

        glBindBuffer(GL_ARRAY_BUFFER, VBO )
        glBufferData(GL_ARRAY_BUFFER, self.teapot_buffer.nbytes, self.teapot_buffer, GL_STATIC_DRAW)

        # teapot vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.teapot_buffer.itemsize * 8, ctypes.c_void_p(0))

        # teapot textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.teapot_buffer.itemsize * 8, ctypes.c_void_p(12))

        # teapot normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.teapot_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)


    def display_instanced(self):

        glUniform1i(self.switcher_loc, 0)


        glDrawArraysInstanced(GL_TRIANGLES,0, len(self.teapot_indicies), self.len_of_instance_array )

    def instanced_textures(self):

        self.texture = glGenTextures(1)

        load_textures("../Textures/blue.jpg", self.texture)



