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


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=(0, 0, 255)):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2),
                self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


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
        pygame.mouse.set_pos(self.width / 2, self.height / 2)

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
                    self.pausemenu(w, h, self.new_graphic_settings.get_state())

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

    def pausemenu(self, width, height, state):

        done = False
        # Set the width and height of the screen [width, height]
        size = (width, height)
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Welcome!")
        font = pygame.font.SysFont('Calibri', 50, False, False)
        settings_button = button((200, 200, 0), width / 2 * 0.8, height / 2 * 0.6, 250, 75, "Settings")
        help_button = button((200, 200, 0), width / 2 * 0.8, height / 2 * 0.9, 250, 75, "Help")
        back_button = button((200, 200, 0), width / 2 * 0.8, height / 2 * 1.2, 250, 75, "Back")

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if settings_button.isOver(mouse_position):
                        settings_button.color = (255, 255, 0)
                    elif back_button.isOver(mouse_position):
                        back_button.color = (255, 255, 0)
                    elif help_button.isOver(mouse_position):
                        help_button.color = (255, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if back_button.isOver(mouse_position):
                        done = True
                        self.new_graphic_settings.first_mouse = True
                        self.new_graphic_settings.mouse_counter = 0


                    elif help_button.isOver(mouse_position):
                        help_page(self.width, self.height)
                        help_button.color = (200, 200, 0)
                        settings_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.6, 250, 75,
                                                 "Settings")
                        help_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.9, 250, 75,
                                             "Help")
                        back_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 1.2, 250, 75,
                                             "Back")
                        screen = pygame.display.set_mode(size, pygame.RESIZABLE)

                    elif settings_button.isOver(mouse_position):
                        self.width, self.height = settings_page(self.width, self.height)
                        settings_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.6, 250, 75,
                                                 "Settings")
                        help_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.9, 250, 75,
                                             "Help")
                        back_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 1.2, 250, 75,
                                             "Back")
                        screen = pygame.display.set_mode(size, pygame.RESIZABLE)

                if event.type == pygame.VIDEORESIZE:
                    # Resizes window

                    if event.w > self.width:
                        self.width = event.w
                        self.height = event.h - 1
                    else:
                        self.width = event.w
                        self.height = event.h

                    settings_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.6, 250, 75,
                                             "Settings")
                    help_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.9, 250, 75, "Help")
                    back_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 1.2, 250, 75, "Back")

            # --- Game logic should go here

            # Background Colour

            self.screen.fill((0, 0, 0))

            # --- Drawing code should go here
            welcome_message = font.render("The game is paused", True, (255, 255, 255))
            self.screen.blit(welcome_message, [self.width / 2 * 0.7, self.height / 5])

            settings_button.draw(self.screen)
            help_button.draw(self.screen)
            back_button.draw(self.screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.new_graphic_settings = improvedGraphics.graphic(self.width, self.height)

        # Return back to saved state
        self.new_graphic_settings.object_locations = state[0]
        self.new_graphic_settings.models_offset = state[1]
        self.new_graphic_settings.models_maxoffset = state[2]

        self.new_graphic_settings.window_resize(self.width, self.height)



"""
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
            pygame.display.flip()"""


def start():
    pygame.init()
    done = False
    width = 1280
    height = 720
    # Set the width and height of the screen [width, height]
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Welcome!")
    font = pygame.font.SysFont('Calibri', 50, False, False)
    start_button = button((200, 200, 0), 500, 1000 / 2 + 50, 250, 75, "Start")
    about_button = button((200, 200, 0), 500, 1000 / 2 - 100, 250, 75, "About")
    help_button = button((200, 200, 0), 500, 1000 / 2 - 225, 250, 75, "Help")
    quit_code = 0

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit_code = 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if start_button.isOver(mouse_position):
                    start_button.color = (255, 255, 0)
                elif about_button.isOver(mouse_position):
                    about_button.color = (255, 255, 0)
                elif help_button.isOver(mouse_position):
                    help_button.color = (255, 255, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if start_button.isOver(mouse_position):
                    done = True
                elif about_button.isOver(mouse_position):
                    about_page()
                    about_button.color = (200, 200, 0)

                elif help_button.isOver(mouse_position):
                    help_page(width, height)
                    help_button.color = (200, 200, 0)

        # --- Game logic should go here

        # Background Colour

        screen.fill((0, 0, 0))

        # --- Drawing code should go here
        welcome_message = font.render("Welcome to the Puzzle Game", True, (255, 255, 255))
        screen.blit(welcome_message, [350, 1000 / 5])

        start_button.draw(screen)
        help_button.draw(screen)
        about_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    if quit_code == 0:  # Start button pressed
        new_game = game(1280, 720, "Main")
        new_game.run()


def about_page():
    font = pygame.font.SysFont('Calibri', 25, False, False)
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    back_button = button((200, 200, 0), 500, 1000 / 2 + 50, 250, 75, "Back")
    done = False

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    back_button.color = (255, 255, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    done = True

        # --- Game logic should go here

        # Background Colour

        screen.fill((0, 0, 0))

        # --- Drawing code should go here
        welcome_message = font.render("This game is inspired by the mobile game - The Room.  ", True, (255, 255, 255))
        welcome_message_two = font.render("This is a 3D interactive puzzle game which you can manipulate objects ",
                                          True, (255, 255, 255))
        welcome_message_three = font.render("and hidden compartments to solve the puzzle.", True, (255, 255, 255))
        last_welcome_message = font.render("Enjoy!", True, (255, 255, 255))
        screen.blit(welcome_message, [350, 1000 / 5])
        screen.blit(welcome_message_two, [250, 1000 / 5 + 30])
        screen.blit(welcome_message_three, [400, 1000 / 5 + 60])
        screen.blit(last_welcome_message, [600, 1000 / 5 + 90])

        back_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


def help_page(width, height):
    font = pygame.font.SysFont('Calibri', 25, False, False)
    size = (width, height)
    screen = pygame.display.set_mode(size)
    back_button = button((200, 200, 0), width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Back")
    done = False

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    back_button.color = (255, 255, 0)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    done = True

        # --- Game logic should go here

        # Background Colour

        screen.fill((0, 0, 0))

        # --- Drawing code should go here
        welcome_message = font.render("Use WASD to move around. w - forward, s - backward, a - left, d - right.  ",
                                      True, (255, 255, 255))
        welcome_message_two = font.render(
            "Click on objects to rotate them. You can move your mouse to look around the room",
            True, (255, 255, 255))
        welcome_message_three = font.render("Press escape to pause the game", True, (255, 255, 255))
        last_welcome_message = font.render("Enjoy!", True, (255, 255, 255))
        screen.blit(welcome_message, [width / 2 * 0.45, height / 2 * 0.4])
        screen.blit(welcome_message_two, [width / 2 * 0.4, height / 2 * 0.6])
        screen.blit(welcome_message_three, [width / 2 * 0.7, height / 2 * 0.8])
        screen.blit(last_welcome_message, [width / 2 * 0.9, height / 2 * 1.0])

        back_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


def settings_page(width, height):
    font = pygame.font.SysFont('Calibri', 50, False, False)
    size = (width, height)
    screen = pygame.display.set_mode(size)

    back_button = button((200, 200, 0), width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Back")
    done = False

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    back_button.color = (255, 255, 0)

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    done = True

        # --- Game logic should go here

        # Background Colour

        screen.fill((0, 0, 0))

        welcome_message = font.render("Settings", True, (255, 255, 255))
        screen.blit(welcome_message, [width / 2 * 0.85, height / 2 * 0.5])

        back_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    return pygame.display.get_window_size()


start()
