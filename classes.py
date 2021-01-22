# Run this file to run the game
# Movement controls are the following: WASD (W for forward A for left, S for backwards, D for right)
# Escape to control your cursor
# Use the mouse to look around. Click on the objects to rotate them.
import os

# Set the windows position
os.environ['SDL_VIDEO_WINDOW_POS'] = '400, 200'
import pygame
from OpenGL.GL import *
from SubFiles import improvedGraphics
import sys



# Class window
class game:

    def __init__(self, width, height, title):
        # Initialise the glfw library

        pygame.init()

        # Setting up the pygame window
        self.screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)

        pygame.event.set_grab(True)
        pygame.mouse.set_visible(True)
        # pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
        pygame.mouse.set_cursor(*pygame.cursors.diamond)

        pygame.display.set_caption(title)
        self.width = width
        self.height = height

        self.new_graphic_settings = improvedGraphics.graphic(width, height)

        self.clock = pygame.time.Clock()

    def run(self):

        done = False
        pygame.mouse.set_pos(self.width/2, self.height/2)

        # Loop
        while not done:

            click = False

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                    w, h = pygame.display.get_surface().get_size()
                    self.pausemenu(w,h)


            self.new_graphic_settings.mouse_move()

            keys_pressed = pygame.key.get_pressed()

            self.new_graphic_settings.player_move(keys_pressed)

            # self.new_graphic_settings.display_instanced()
            self.new_graphic_settings.display()

            if click:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                self.new_graphic_settings.pick(mouse_x, mouse_y)

            glBindFramebuffer(GL_FRAMEBUFFER, 0)

            pygame.display.flip()

            self.clock.tick(60)

        # Ends pygame
        pygame.quit()

    def pausemenu(self, width, height):

        pygame.display.set_caption("Pause Menu")
        running = False
        pygame.event.set_grab(False)
        self.width = width
        self.height = height




        while not running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                    self.new_graphic_settings.first_mouse = True
                    self.new_graphic_settings.mouse_counter = 0
                    pygame.mouse.set_pos(self.width/2, self.height/2)

                    running = True

                if event.type == pygame.VIDEORESIZE:
                    # Resizes window
                    if event.w > self.width:
                        self.width = event.w
                        self.height = event.h - 1
                    else:
                        self.width = event.w
                        self.height = event.h
                    self.new_graphic_settings.window_resize(self.width, self.height)



            self.screen.fill((0,0,0))
            pygame.display.flip()


new_game = game(1280, 720, "Main")
new_game.run()
