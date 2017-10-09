import pygame

from pygame import Color
from src.bone import Bone

class Skeleton:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.screen.fill(Color('white'))

        bones = Bone(self.screen, None, 10, 20, 300, 120)

        pygame.display.flip()
        pygame.display.update()
