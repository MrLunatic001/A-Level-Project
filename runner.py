# Run this file to run the game
# Use the mouse to look around. Click on the objects to rotate them.
import os
import pygame
from OpenGL.GL import *
from SubFiles import level1Graphics, level2Graphics
import sys


pygame.init()
resolution = pygame.display.Info()
screen_size = str(resolution.current_w / 2) + str(resolution.current_h / 2)
# Set the windows position
os.environ['SDL_VIDEO_WINDOW_POS'] = screen_size
dir = r"C:\Users\User\Documents\GitHub\A-Level-Project\SubFiles"
path = os.path.join(dir, "savestate.txt")


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
        self.new_graphic_settings = level1Graphics.graphic(width, height, self.inventory_choice)
        self.level_counter = 0

        self.clock = pygame.time.Clock()

    def run(self):

        done = False
        pygame.mouse.set_pos(self.width / 2, self.height / 2)

        pygame.mixer.set_num_channels(7)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("Audio/background.mp3"), -1)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("Audio/soundtrack.mp3"), -1)
        pygame.mixer.Channel(2).play(pygame.mixer.Sound("Audio/walk.mp3"), -1)
        pygame.mixer.Channel(1).set_volume(0.3)
        pygame.mixer.Channel(2).pause()

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    self.new_graphic_settings.noclip = not self.new_graphic_settings.noclip

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
            if keys_pressed[pygame.K_w] or keys_pressed[pygame.K_a] or keys_pressed[pygame.K_d] or keys_pressed[
                pygame.K_s]:
                if not play:
                    play = True
                    pygame.mixer.Channel(2).unpause()
            else:
                pygame.mixer.Channel(2).pause()
                play = False

            if click:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                self.new_graphic_settings.pick(mouse_x, mouse_y)

            glBindFramebuffer(GL_FRAMEBUFFER, 0)

            pygame.display.flip()

            self.clock.tick(60)
            self.save_game()


        self.game_over(self.width, self.height)

    def next_level(self, width, height):
        font = pygame.font.SysFont('Calibri', 50, True, False)
        pygame.display.set_caption("Continue")
        size = (width, height)
        SAPPHIRE = (15, 82, 186)
        GRAPEFRUIT = (224, 112, 124)
        screen = pygame.display.set_mode(size)
        welcome_message = font.render("Next Level?", True, SAPPHIRE)

        continue_button = button(GRAPEFRUIT, width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Continue")
        done = False

        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if continue_button.isOver(mouse_position):
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
            mouse_position = pygame.mouse.get_pos()

            if continue_button.isOver(mouse_position):
                continue_button.color = (254, 132, 154)
            else:
                continue_button.color = GRAPEFRUIT

            # Background Colour

            screen.fill((0, 180, 180))

            screen.blit(welcome_message, [width / 2 * 0.8, height / 2 * 0.5])

            continue_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.new_graphic_settings = level2Graphics.graphic(self.width, self.height, 0)
        pygame.display.set_caption("Game")

    def pausemenu(self, width, height, state):

        done = False
        # Set the width and height of the screen [width, height]
        size = (width, height)
        CORALBLUE = (0, 255, 180, 0.8)
        GRAPEFRUIT = (224, 112, 124)
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("Paused")
        font = pygame.font.SysFont('Calibri', 50, False, False)

        help_button = button(CORALBLUE, width / 2 * 0.8, height / 2 * 0.9, 250, 75, "Controls")
        back_button = button(GRAPEFRUIT, width / 2 * 0.8, height / 2 * 1.2, 250, 75, "Back")

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_position = pygame.mouse.get_pos()
                    if back_button.isOver(mouse_position):
                        done = True
                        self.new_graphic_settings.first_mouse = True
                        self.new_graphic_settings.mouse_counter = 0

                    elif help_button.isOver(mouse_position):
                        help_page(self.width, self.height)
                        pygame.display.set_caption("Paused")

                if event.type == pygame.VIDEORESIZE:
                    # Resizes window

                    if event.w > self.width:
                        self.width = event.w
                        self.height = event.h - 1
                    else:
                        self.width = event.w
                        self.height = event.h


            # --- Game logic should go here

            mouse_position = pygame.mouse.get_pos()
            if help_button.isOver(mouse_position):
                help_button.color = (150, 255, 180)
            else:
                help_button.color = (0, 255, 180, 0.8)
            if back_button.isOver(mouse_position):
                back_button.color = (254, 132, 154)
            else:
                back_button.color = GRAPEFRUIT

            # Background Colour

            self.screen.fill((0, 180, 180))

            # --- Drawing code should go here
            welcome_message = font.render("The game is paused", True, (15, 82, 186))
            self.screen.blit(welcome_message, [self.width / 2 * 0.7, self.height / 5])

            help_button.draw(self.screen)
            back_button.draw(self.screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        self.save_state(state, self.level_counter)

    def game_over(self, width, height):
        font = pygame.font.SysFont('Calibri', 50, False, False)
        size = (width, height)
        BROWN = (139, 69, 19)
        GRAPEFRUIT = (224, 112, 124)
        CORALBLUE = (0, 255, 180, 0.8)
        quited = False
        screen = pygame.display.set_mode(size)
        welcome_message = font.render("Game Completed!", True, BROWN)
        welcome_message_one = font.render("Thank you for playing.", True, BROWN)
        welcome_message_two = font.render("I hope you enjoyed playing this game.", True, BROWN)

        quit = button(GRAPEFRUIT, width / 2 * 0.8, height / 2 * 1.7, 250, 75, "Quit")
        menu = button(CORALBLUE, width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Main Menu")
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
            mouse_position = pygame.mouse.get_pos()
            if quit.isOver(mouse_position):
                quit.color = (254, 132, 154)
            else:
                quit.color = GRAPEFRUIT
            if menu.isOver(mouse_position):
                menu.color = (150, 255, 180)
            else:
                menu.color = CORALBLUE

            # Background Colour

            screen.fill((237, 201, 175))

            screen.blit(welcome_message, [width / 2 * 0.7, height / 2 * 0.5])
            screen.blit(welcome_message_one, [width / 2 * 0.65, height / 2 * 0.7])
            screen.blit(welcome_message_two, [width / 2 * 0.4, height / 2 * 0.9])

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

        PURPLE = (188,93,255)
        GRAPEFRUIT = (244, 112, 124)
        screen = pygame.display.set_mode(size)
        welcome_message = font.render("Inventory", True, PURPLE)

        location = [[width / 2 * 0.4, height / 2 *0.75], [width / 2 * 0.9, height / 2*0.75], [width / 2 * 1.4, height / 2*0.75]]
        hammer = pygame.transform.scale(pygame.image.load('Textures/hammer.png'), (130, 130))
        empty = pygame.transform.scale(pygame.image.load('Textures/empty.png'), (130, 130))
        key = pygame.transform.scale(pygame.image.load('Textures/key.png'), (130, 130))


        back_button = button(GRAPEFRUIT, width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Back")
        done = False

        while not done:
            # --- Main event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
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

            mouse_position = pygame.mouse.get_pos()
            if back_button.isOver(mouse_position):
                back_button.color = (254, 132, 154)
            else:
                back_button.color = GRAPEFRUIT

            # Background Colour

            screen.fill((0, 50, 160))

            # Displays inventory slot

            # Displays chosen item

            pygame.draw.rect(screen, (0, 65, 175),
                             (location[self.inventory_choice][0], location[self.inventory_choice][1], 140, 140), 0)

            for i in range(3):
                if inventory[i] == 0:
                    screen.blit(empty, location[i])
                elif inventory[i] == 1:
                    screen.blit(hammer, location[i])
                elif inventory[i] == 2:
                    screen.blit(key, location[i])

            screen.blit(welcome_message, [width / 2 * 0.85, height / 2 * 0.25])


            back_button.draw(screen)

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

        self.save_state(state, self.level_counter)

    def save_state(self, state, level):

        self.screen = pygame.display.set_mode((self.width, self.height), pygame.OPENGL | pygame.DOUBLEBUF)
        if level == 0:
            self.new_graphic_settings = level1Graphics.graphic(self.width, self.height, self.inventory_choice)

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
        pygame.display.set_caption("Main")

    def save_game(self):
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name == "savestate.txt":
                    print("saving")
                    state = self.new_graphic_settings.get_state()

                    f = open(path, "w")
                    f.truncate(0)
                    f.close()
                    f = open(path, "w")
                    for i in range(12):
                        f.write(str(state[i])+'\n')
                        f.write('\n')

                    f.close()



def start():
    done = False
    width = 1280
    height = 720
    CORALBLUE = (0, 255, 180, 0.8)
    # Set the width and height of the screen [width, height]
    size = (width, height)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Main Menu")
    font = pygame.font.SysFont('Calibri', 50, False, False)
    start_button = button((244,128,55, 0.8), 500, 1000 / 2 + 50, 250, 75, "Start")
    about_button = button(CORALBLUE, 500, 1000 / 2 - 90, 250, 75, "About")
    help_button = button(CORALBLUE, 500, 1000 / 2 - 225, 250, 75, "Controls")
    quit_code = 0

    loadstate = False

    for root, dirs, files in os.walk(dir):
        for name in files:
            if name == "savestate.txt":
                loadstate = True
                f = open(path, "r")
                state = f.read()
                f.close()
    if not loadstate:

        f = open(path, "w")
        f.write("null")
        f.close()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit_code = 1

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if start_button.isOver(mouse_position):
                    done = True
                elif about_button.isOver(mouse_position):
                    about_page()
                    pygame.display.set_caption("Main Menu")
                elif help_button.isOver(mouse_position):
                    help_page(width, height)
                    pygame.display.set_caption("Main Menu")

        # --- Game logic should go here
        # Changes button colour if mouse if hovered over them
        mouse_position = pygame.mouse.get_pos()
        if start_button.isOver(mouse_position):
            start_button.color = (254,138,65, 0.8)
        else:
            start_button.color = (224,128,55, 0.8)
        if about_button.isOver(mouse_position):
            about_button.color = (150, 255, 180)
        else:
            about_button.color = CORALBLUE
        if help_button.isOver(mouse_position):
            help_button.color = (150, 255, 180)
        else:
            help_button.color = CORALBLUE


        # Background Colour

        screen.fill((0, 180, 180))

        # --- Drawing code should go here
        welcome_message = font.render("Welcome to the Puzzle Game", True, (0, 70, 220))
        screen.blit(welcome_message, [350, 1000 / 5])



        start_button.draw(screen)
        help_button.draw(screen)
        about_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    if quit_code == 0:  # Start button pressed
        new_game = game(1280, 720, "Game")
        new_game.run()




def about_page():
    font = pygame.font.SysFont('Calibri', 25, True, False)
    pygame.display.set_caption("About")
    size = (1280, 720)
    screen = pygame.display.set_mode(size)
    GRAPEFRUIT = (224, 112, 124)
    SAPPHIRE = (15, 82, 186)
    back_button = button(GRAPEFRUIT, 500, 1000 / 2 + 50, 250, 75, "Back")
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
        mouse_position = pygame.mouse.get_pos()
        if back_button.isOver(mouse_position):
            back_button.color = (254, 132, 154)
        else:
            back_button.color = GRAPEFRUIT

        # Background Colour

        screen.fill((0, 180, 180))

        # --- Drawing code should go here
        welcome_message = font.render(
            "This game is inspired by the mobile game - The Room and a souvenir that I bought  ", True, SAPPHIRE)
        welcome_message_two = font.render(
            " in Greece a long time ago. This is a 3D interactive game which you can manipulate objects ",
            True, SAPPHIRE)
        welcome_message_three = font.render("to solve the puzzle. Enjoy!", True, SAPPHIRE)

        screen.blit(welcome_message, [250, 1000 / 5])
        screen.blit(welcome_message_two, [200, 1000 / 5 + 30])
        screen.blit(welcome_message_three, [1080/2 - 50, 1000 / 5 + 60])


        back_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


def help_page(width, height):
    font = pygame.font.SysFont('Calibri', 25, True, False)
    pygame.display.set_caption("Controls")
    size = (width, height)
    GRAPEFRUIT = (224, 112, 124)
    SAPPHIRE = (15, 82, 186)
    screen = pygame.display.set_mode(size)
    back_button = button(GRAPEFRUIT, width / 2 * 0.8, height / 2 * 1.4, 250, 75, "Back")
    done = False

    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_position = pygame.mouse.get_pos()
                if back_button.isOver(mouse_position):
                    done = True

        # --- Game logic should go here

        mouse_position = pygame.mouse.get_pos()
        if back_button.isOver(mouse_position):
            back_button.color = (254, 132, 154)
        else:
            back_button.color = GRAPEFRUIT

        # Background Colour

        screen.fill((0, 180, 180))

        # --- Drawing code should go here
        welcome_message = font.render(
            "Use WASD to move around. w - forward, s - backward, a - left, d - right, e - inventory.  ",
            True, SAPPHIRE)
        welcome_message_two = font.render(
            "CLICK on objects to rotate/ move them.",
            True, SAPPHIRE)
        welcome_message_three = font.render("Press escape to pause the game", True, SAPPHIRE)
        last_welcome_message = font.render("Equip items in the inventory by pressing 1,2,3", True, SAPPHIRE)

        screen.blit(welcome_message, [width / 2 * 0.38, height / 2 * 0.4])
        screen.blit(welcome_message_two, [width / 2 * 0.74, height / 2 * 0.6])
        screen.blit(welcome_message_three, [width / 2 * 0.74, height / 2 * 0.8])
        screen.blit(last_welcome_message, [width / 2 * 0.65, height / 2 * 1.0])

        back_button.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()


start()
f = open(path, "r")
for lines in f:
    print(lines)
f.close()