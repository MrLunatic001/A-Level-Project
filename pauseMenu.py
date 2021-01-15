import pygame
from pygame.locals import *




def run( width, height):
    BLACK = (0, 0, 0)
    size = (width, height)
    screen = pygame.display.set_mode(size, RESIZABLE)
    pygame.display.set_caption("Pause Menu")
    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                w, h = pygame.display.get_surface().get_size()
                pygame.mouse.set_pos(w/2, h/2)
                done = True

        screen.fill(BLACK)
        pygame.display.flip()
        clock.tick(60)




