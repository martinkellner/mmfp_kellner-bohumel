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
        self._startPointCircle = None
        self._endPointCircle = None

        self.draw()
        self.__repr__()

    def __repr__(self):
        print(str(self.startX) + ' ' + str(self.startY) + '\n' + str(self.endX) + ' ' + str(self.endY))

    def draw(self):
        pygame.draw.line(self._screen, self._color, (self.startX, self.startY), (self.endX, self.endY), 2)
        if self._endPointCircle != None and self._startPointCircle != None:
            self.drawEndPoints()

    def drawEndPoints(self):
        self._startPointCircle = pygame.draw.circle(self._screen, self._color,(int(self.startX), int(self.startY)), 5, 1)
        self._endPointCircle = pygame.draw.circle(self._screen, self._color, (int(self.endX), int(self.endY)), 5, 1)

    def removeEndPoints(self):
        self._startPointCircle = None
        self._endPointCircle = None

    def isOnHover(self, x, y):
        ##TODO: calculate if point given by x,y is near to line segment
        pass