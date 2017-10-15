import pygame

from pygame import Color
from src.bone import Bone

class Skeleton:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill(Color('white'))

        root = Bone(self.screen, True, 10, 90, 250, 200, None)
        bone0 = Bone(self.screen, False, 100, 90, None, None, root)
        bone1 = Bone(self.screen, False, 50, 45, None, None, root)
        bone2 = Bone(self.screen, False, 50, 135, None, None, root)
        bone4 = Bone(self.screen, False, 50, 45, None, None, bone0)
        bone5 = Bone(self.screen, False, 50, 135, None, None, bone0)

        pygame.display.flip()
        pygame.display.update()
