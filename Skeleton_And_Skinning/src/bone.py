import pygame
from math import cos, sin, atan2, sqrt


import numpy as np
from pygame import Color

class Bone:

    def __init__(self, screen, length, angle, sVector=None, parent=None):

        self._sVector = parent._eVector if parent != None else sVector
        self._eVector = [None, None, 1]
        self._angle = angle
        self._sAngle = self._angle - parent._angle if parent != None else self._angle
        self._dAngle = 0.0
        self._lenght = length
        self._parent = parent
        self._children = []
        self._countChildren = 0

        self.CalculateEVector()

        self._screen = screen
        self._color = Color('red') if parent == None else Color('black')
        self._shColor = Color(0, 208, 119, 32)
        self._selected = False

        self._endPointCircle = None
        self._shadow = None

        if self._parent != None:
            self._parent.AddChild(self)

        self._wMatrix = None
        self.ReceiveWMatrix()

    def __str__(self):
        return '[( ' + str(self._sVector[0]) + ', ' + str(self._sVector[1]) + '),( ' + str(self._eVector[0]) + ', ' + str(self._eVector[1]) + ')]'

    def __repr__(self):
        print(str(self._sVector[0]) + ' ' + str(self._sVector[1]) + '\n' + str(self._eVector[0]) + ' ' + str(self._eVector[1]))

    def Draw(self):
        pygame.draw.line(self._screen, self._color, (self._sVector[0], self._sVector[1]),
                         (self._eVector[0], self._eVector[1]), 2 if self._endPointCircle == None else 3)
        if self._endPointCircle != None:
               self.DrawEndPoints()

    def DrawEndPoints(self):
        self._endPointCircle = pygame.draw.circle(self._screen, self._color, (int(self._eVector[0]), int(self._eVector[1])), 6, 2 if self._selected else 0 )

    def RemoveEndPoints(self):
        self._endPointCircle = None

    def IsOnHover(self, x, y):
        test0 = ((x - self._eVector[0])**2 + (y - self._eVector[1])**2) <= 3.5**2
        if test0:
            return True
        else:
            test1 = abs((self._eVector[1] - self._sVector[1])*x - (self._eVector[0] - self._sVector[0])*y + self._eVector[0]*self._sVector[1] - self._eVector[1]*self._sVector[0])/sqrt((self._eVector[1] - self._sVector[1])**2 + (self._eVector[0] - self._sVector[0])**2)
            if not (test1 < 3):
                return False
            minX = min(self._sVector[0], self._eVector[0])
            minY = min(self._sVector[1], self._eVector[1])
            test2 = (minX - 3 < x < (self._sVector[0] if minX == self._eVector[0] else self._eVector[0]) + 3) and (minY - 3 < y < (self._sVector[1] if minY == self._eVector[1] else self._eVector[1]) + 3)
            if test2:
                return True
            return False

    def AddChild(self, bone):
        self._children.append(bone)
        self._countChildren += 1

    def CalculateEVector(self):
        self._eVector[0] = self._sVector[0] + (self._lenght * cos(self._angle if self._parent == None else self._sAngle + self._parent._angle))
        self._eVector[1] = self._sVector[1] + (self._lenght * sin(self._angle if self._parent == None else self._sAngle + self._parent._angle))

    def Move(self, eM_Vector):
        xDelta = eM_Vector[0] - self._sVector[0]
        yDelta = eM_Vector[1] - self._sVector[1]

        _angle = atan2(yDelta, xDelta)
        self._dAngle = self._sAngle = _angle - self._angle
        self.ReCalwMatrix()
        self._angle = _angle
        if self._parent != None:
            self._sAngle = self._angle - self._parent._angle
        savParent = self._parent; self._parent = None
        self.CalculateEVector()
        self._parent = savParent
        self.MoveChilder()

    def MoveChilder(self):
        for _ch in self._children:
            _ch._angle = self._angle + _ch._sAngle
            _ch.CalculateEVector()
            _ch.ReCalwMatrix()
            _ch.MoveChilder()
            _ch._dAngle = 0.0

    def ReceiveWMatrix(self):
        sinA = sin(self._dAngle)
        cosA = cos(self._dAngle)
        self._wMatrix = np.array([
            [cosA, -1*sinA, -1*cosA*self._sVector[0] + sinA*self._sVector[1] + self._sVector[0]],
            [sinA,    cosA, -1*sinA*self._sVector[0] - cosA*self._sVector[1] + self._sVector[1]],
            [   0,       0,                                                                  1]
        ])

    def ReCalwMatrix(self):
        self.ReceiveWMatrix()
        if self._parent != None:
            self._wMatrix = np.dot(self._parent._wMatrix, self._wMatrix)
