import pygame

from pygame import Color
from src.bone import Bone

class Skeleton:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.screen.fill(Color('white'))

        root = Bone(self.screen, True, 10, 20, 300, 120, None)
        bone0 = Bone(self.screen, False, None, None, 50, 60, root)
        bone1 = Bone(self.screen, False, None, None, -30, 80, root)
        bone2 = Bone(self.screen, False, None, None, 30, 80, bone1)

        pygame.display.flip()
        pygame.display.update()
