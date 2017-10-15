import pygame
import numpy as np
import math

from pygame import Color

class Bone:

    def __init__(self, screen, root, length, angle, startX=None, startY=None, parent=None):

        self.startX = startX if root else parent.endX
        self.startY = startY if root else parent.endY
        self.angle = angle  # degree
        self.radius = np.radians(self.angle)
        self.length = length

        # The ending point is calculated.
        self.endX = self.startX + self.length * math.cos(self.radius)
        self.endY = self.startY + self.length * math.sin(self.radius)

        self.parent = parent
        self.root = root

        self._screen = screen
        self._color = Color('red') if root else Color('black')

        self.draw()
        self.__repr__()

    def __repr__(self):
        print(str(self.startX) + ' ' + str(self.startY) + '\n' + str(self.endX) + ' ' + str(self.endY))

    def draw(self):
        pygame.draw.line(self._screen, self._color, (self.startX, self.startY), (self.endX, self.endY))
