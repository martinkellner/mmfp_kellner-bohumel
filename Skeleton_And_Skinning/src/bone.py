import pygame

from pygame import Color

class Bone:

    def __init__(self, screen, root, x1, y1, x2, y2, parent=None):

        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

        self.parent = parent
        self.root = root
        self._screen = screen
        self._color = Color('red') if root else Color('black')

        if (self.root == True):
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2
        else:
            if (self.parent == None):
                raise Exception('The bone ' + self.__repr__() + ' is not a root, missing a parent bone')
            else:
                if (parent.x2 == None or parent.y2 == None):
                    raise Exception('Missing coordinates parent.x2, parent.y2, bone is not a root')
                if (x2 == None or y2 == None):
                    raise Exception('Missing coordinates x2, y2, bone is not a root')
                self.x1 = parent.x2
                self.y1 = parent.y2
                self.x2 = x2 + self.x1
                self.y2 = y2 + self.y1

        self.draw()
        self.__repr__()

    def __repr__(self):
        print(str(self.x1) + ' ' + str(self.y1) + '\n' + str(self.x2) + ' ' + str(self.y2))

    def draw(self):
        pygame.draw.line(self._screen, self._color, (self.x1, self.y1), (self.x2, self.y2))
