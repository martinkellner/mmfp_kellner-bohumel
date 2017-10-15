import pygame

from pygame import Color
from src.bone import Bone

class Skeleton:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.screen.fill(Color('white'))

        root = Bone(self.screen, True, 10, 20, 300, 120, None)
        bones = Bone(self.screen, False, None, None, 400, 220, root)

        pygame.display.flip()
        pygame.display.update()
