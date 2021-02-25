# Run this file to run the game
# Use the mouse to look around. Click on the objects to rotate them.
import os

# Set the windows position
os.environ['SDL_VIDEO_WINDOW_POS'] = '400, 200'
import pygame
from OpenGL.GL import *
from SubFiles import improvedGraphics, level2Graphics
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
        self.inventory_choice = 0
        self.new_graphic_settings = improvedGraphics.graphic(width, height, self.inventory_choice)
        self.level_counter = 0

        self.clock = pygame.time.Clock()

    def run(self):

        done = False
        pygame.mouse.set_pos(self.width / 2, self.height / 2)
        walk_sound = pygame.mixer.Sound("Audio/walk.mp3")
        pygame.mixer.music.load("Audio/background.mp3")
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1, 0.0)
        play = False

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                    w, h = pygame.display.get_surface().get_size()
                    self.inventory(w, h, self.new_graphic_settings.get_state())



            # Checks if level is finished
            if self.new_graphic_settings.checkwin():
                if self.level_counter == 0:
                    self.inventory_choice = 0
                    self.level_counter += 1
                    self.next_level(self.width, self.height)
                else:
                    done = True


            self.new_graphic_settings.mouse_move()

            keys_pressed = pygame.key.get_pressed()

            self.new_graphic_settings.player_move(keys_pressed)

            # self.new_graphic_settings.display_instanced()
            self.new_graphic_settings.display()

            # Play walking sound if walking
            if keys_pressed[pygame.K_w] or  keys_pressed[pygame.K_a] or  keys_pressed[pygame.K_d] or keys_pressed[pygame.K_s]:
                if not play:
                    play = True
                    walk_sound.play(-1)
            else:
                walk_sound.stop()
                play = False

            if click:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                self.new_graphic_settings.pick(mouse_x, mouse_y)

            glBindFramebuffer(GL_FRAMEBUFFER, 0)

            pygame.display.flip()

            self.clock.tick(60)

        self.game_over(self.width, self.height)





    def next_level(self, width, height):
        font = pygame.font.SysFont('Calibri', 50, False, False)
        size = (width, height)
        WHITE = (255, 255, 255)
        screen = pygame.display.set_mode(size)
        welcome_message = font.render("Next Level?", True, WHITE)

        back_button = button((200, 200, 0), width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Continue")
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
                if event.type == pygame.KEYDOWN:
                    # Chooses inventory slot
                    if event.key == pygame.K_1:
                        self.inventory_choice = 0
                    elif event.key == pygame.K_2:
                        self.inventory_choice = 1
                    elif event.key == pygame.K_3:
                        self.inventory_choice = 2

            # --- Game logic should go here

            # Background Colour

            screen.fill((100, 100, 100))



            screen.blit(welcome_message, [width / 2 * 0.8, height / 2 * 0.5])


            back_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.new_graphic_settings = level2Graphics.graphic(self.width, self.height, 0)

    def pausemenu(self, width, height, state):

        done = False
        # Set the width and height of the screen [width, height]
        size = (width, height)
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Welcome!")
        font = pygame.font.SysFont('Calibri', 50, False, False)

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
                    if back_button.isOver(mouse_position):
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
                        pygame.display.set_mode(size, pygame.RESIZABLE)

                if event.type == pygame.VIDEORESIZE:
                    # Resizes window

                    if event.w > self.width:
                        self.width = event.w
                        self.height = event.h - 1
                    else:
                        self.width = event.w
                        self.height = event.h

                    help_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 0.9, 250, 75, "Help")
                    back_button = button((200, 200, 0), self.width / 2 * 0.8, self.height / 2 * 1.2, 250, 75, "Back")

            # --- Game logic should go here

            # Background Colour

            self.screen.fill((0, 0, 0))

            # --- Drawing code should go here
            welcome_message = font.render("The game is paused", True, (255, 255, 255))
            self.screen.blit(welcome_message, [self.width / 2 * 0.7, self.height / 5])

            help_button.draw(self.screen)
            back_button.draw(self.screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        self.save_state(state, self.level_counter)

    def game_over(self, width, height):
        font = pygame.font.SysFont('Calibri', 50, False, False)
        size = (width, height)
        BROWN = (139,69,19)
        quited = False
        screen = pygame.display.set_mode(size)
        welcome_message = font.render("Game Completed!", True, BROWN)
        welcome_message_one = font.render("Thank you for playing.", True, BROWN)
        welcome_message_two = font.render("I hope you enjoyed playing this game.", True, BROWN)

        quit = button((200, 200, 0), width / 2 * 0.8, height / 2 * 1.4, 250, 75, "quit")
        menu = button((200, 200, 0), width / 2 * 0.8, height / 2 * 1.7, 250, 75, "Main Menu")
        done = False

        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    if quit.isOver(mouse_position):
                        quit.color = (255, 255, 0)
                    if menu.isOver(mouse_position):
                        menu.color = (255, 255, 0)
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if quit.isOver(mouse_position):
                        done = True
                        quited = True
                    if menu.isOver(mouse_position):
                        done = True

            # --- Game logic should go here

            # Background Colour

            screen.fill((237, 201, 175))

            screen.blit(welcome_message, [width / 2 * 0.65, height / 2 * 0.5])
            screen.blit(welcome_message_one, [width / 2 * 0.6, height / 2 * 0.7])
            screen.blit(welcome_message_two, [width / 2 * 0.35, height / 2 * 0.9])

            quit.draw(screen)
            menu.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        if quited:
            sys.exit()
        else:
            start()

    def inventory(self, width, height, state):
        inventory = state[10]
        font = pygame.font.SysFont('Calibri', 50, False, False)
        size = (width, height)
        WHITE = (255, 255, 255)
        screen = pygame.display.set_mode(size)
        welcome_message = font.render("Inventory", True, WHITE)
        slot_one = font.render("1", True, WHITE)
        slot_two = font.render("2", True, WHITE)
        slot_three = font.render("3", True, WHITE)
        location = [[width / 2 * 0.45, height / 2], [width / 2 * 0.95, height / 2], [width / 2 * 1.45, height / 2]]
        hammer = pygame.transform.scale(pygame.image.load('Textures/hammer.png'), (95, 95))
        empty = pygame.transform.scale(pygame.image.load('Textures/empty.png'), (95, 95))
        key = pygame.transform.scale(pygame.image.load('Textures/key.png'), (95, 95))

        rect_pos = [width / 2 * 0.45, height / 2]

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
                if event.type == pygame.KEYDOWN:
                    # Chooses inventory slot
                    if event.key == pygame.K_1:
                        self.inventory_choice = 0
                    elif event.key == pygame.K_2:
                        self.inventory_choice = 1
                    elif event.key == pygame.K_3:
                        self.inventory_choice = 2

            # --- Game logic should go here

            # Background Colour

            screen.fill((100, 100, 100))

            # Displays inventory slot

            pygame.draw.rect(screen, (0, 255, 0),
                             (location[self.inventory_choice][0], location[self.inventory_choice][1], 101, 101), 0)
            pygame.draw.rect(screen, (100, 100, 100),
                             (location[self.inventory_choice][0], location[self.inventory_choice][1], 99, 99), 0)

            for i in range(3):
                if inventory[i] == 0:
                    screen.blit(empty, location[i])
                elif inventory[i] == 1:
                    screen.blit(hammer, location[i])
                elif inventory[i] == 2:
                    screen.blit(key, location[i])

            screen.blit(welcome_message, [width / 2 * 0.9, height / 2 * 0.5])
            screen.blit(slot_one, [width / 2 * 0.5, height / 2 * 0.7])
            screen.blit(slot_two, [width / 2, height / 2 * 0.7])
            screen.blit(slot_three, [width / 2 * 1.5, height / 2 * 0.7])

            back_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        self.save_state(state, self.level_counter)

    def save_state(self, state, level):

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        if level == 0:
            self.new_graphic_settings = improvedGraphics.graphic(self.width, self.height, self.inventory_choice)

        elif level == 1:
            self.new_graphic_settings = level2Graphics.graphic(self.width, self.height, self.inventory_choice)
            self.new_graphic_settings.key_inserted = state[12]
        # Return back to saved state
        self.new_graphic_settings.object_locations = state[0]
        self.new_graphic_settings.models_offset = state[1]
        self.new_graphic_settings.models_maxoffset = state[2]
        self.new_graphic_settings.models = state[3]
        self.new_graphic_settings.cam.camera_pos = state[4]
        self.new_graphic_settings.cam.camera_up = state[5]
        self.new_graphic_settings.cam.camera_front = state[6]
        self.new_graphic_settings.cam.camera_right = state[7]
        self.new_graphic_settings.cam.jaw = state[8]
        self.new_graphic_settings.cam.pitch = state[9]
        self.new_graphic_settings.inventory = state[10]
        self.new_graphic_settings.pick_boolean = state[11]

        self.new_graphic_settings.window_resize(self.width, self.height)


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
        welcome_message = font.render("This game is inspired by the mobile game - The Room and a souvenir that I bought  ", True, (255, 255, 255))
        welcome_message_two = font.render(" in Greece a long time ago. This is a 3D interactive game which you can manipulate objects ",
                                          True, (255, 255, 255))
        welcome_message_three = font.render("and hidden compartments to solve the puzzle.", True, (255, 255, 255))
        last_welcome_message = font.render("Enjoy!", True, (255, 255, 255))
        screen.blit(welcome_message, [250, 1000 / 5])
        screen.blit(welcome_message_two, [200, 1000 / 5 + 30])
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
        welcome_message = font.render(
            "Use WASD to move around. w - forward, s - backward, a - left, d - right, e - inventory.  ",
            True, (255, 255, 255))
        welcome_message_two = font.render(
            "Click on objects to rotate them. You can move your mouse to look around the room",
            True, (255, 255, 255))
        welcome_message_three = font.render("Press escape to pause the game", True, (255, 255, 255))
        last_welcome_message = font.render("You can only move objects with your hand (empty slot in inventory)!", True, (255, 255, 255))

        screen.blit(welcome_message, [width / 2 * 0.4 , height / 2 * 0.4])
        screen.blit(welcome_message_two, [width / 2 * 0.4, height / 2 * 0.6])
        screen.blit(welcome_message_three, [width / 2 * 0.7, height / 2 * 0.8])
        screen.blit(last_welcome_message, [width / 2 * 0.4, height / 2 * 1.0])

        back_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()



start()
