import pygame

from pygame import Color

class Bone:

    def __init__(self, screen, parent, x0=0, x1=0, y0=0, y1=0):

        self._parent = parent
        self._children = []
        self._screen = screen

        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1

        self.draw()
        self.__repr__()

    def __repr__(self):
        print(str(self._x0) + ' ' + str(self._x1) + '\n' + str(self._y0) + ' ' + str(self._y1))

    def draw(self):
        pygame.draw.line(self._screen, Color('black'), (self._x0, self._x1), (self._y0, self._y1))
