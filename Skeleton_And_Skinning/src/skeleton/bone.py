import pygame
import numpy as np

from math import cos, sin, atan2, sqrt
from pygame import Color

''' Trieda reprezentujucu kost '''
class Bone:

    # Konstruktor
    def __init__(self, id, screen, length, angle, sVector=None, parent=None):
        self._id = id # ID kost
        # Vektor prveho bodu, bud od otca alebo ak je root, tak svoj
        self._sVector = parent._eVector if parent != None else sVector
        # Pole pre koncovy vektor, bude vypocitany
        self._eVector = [None, None, 1]
        self._angle = angle # Uhol
        # Uhol medzi kostou a otcovskou kostou
        self._sAngle = self._angle - parent._angle if parent != None else self._angle
        self._dAngle = 0.0  # Pomocna premenna
        self._lenght = length # Dlzka
        self._parent = parent # otec kosti
        self._children = []   # deti kosti

        # Vypocitaj koncovy vektor
        self.CalculateEVector()
        # Graficka plocha kniznice pyGame
        self._screen = screen
        # Farba kosti
        self._color = Color('red') if parent == None else Color('black')
        self._selected = False # Premenna hovori, ci je kost vybrana

        self._endPointCircle = None # Zviditelne koncove body, zviditelnenie ci je kost vybrana, alebo sa na nu ukazuje
        # Ak ma kost otca, tak otcovi pridaj tuto kost ako dieta
        if self._parent != None:
            self._parent.AddChild(self)

        # World Matrix kosti
        self._wMatrix = None
        # Ziskaj maticu sveta kosti
        self.ReceiveWMatrix()

    # Textova reprezentacia objektu
    def __str__(self):
        return '[( ' + str(self._sVector[0]) + ', ' + str(self._sVector[1]) + '),( ' + str(self._eVector[0]) + ', ' + str(self._eVector[1]) + ')]'

    # Vykresli kost
    def Draw(self):
        # Kresli ciaru
        pygame.draw.line(self._screen, self._color, (self._sVector[0], self._sVector[1]),
                         (self._eVector[0], self._eVector[1]), 2 if self._endPointCircle == None else 3)
        # Kresli koncove body, ak je kost vybrana
        if self._endPointCircle != None:
            self.DrawEndPoints()

    # Kresli koncove body
    def DrawEndPoints(self):
        self._endPointCircle = pygame.draw.circle(self._screen, self._color, (int(self._eVector[0]), int(self._eVector[1])), 6, 2 if self._selected else 0 )

    # Zmaz koncove body
    def RemoveEndPoints(self):
        self._endPointCircle = None

    # Vrati kost True, ak na kost je ukazovane mysou
    def IsOnHover(self, x, y):
        # True, ak ukazujes v blizkosti koncoveho vektora
        test0 = ((x - self._eVector[0])**2 + (y - self._eVector[1])**2) <= 3.5**2
        if test0:
            return True
        else:
            # Test ci je na vzdialeny bod mysi od priamku urcenej dvoma vektromi (start, end) kosti viac ako 3 ak ano tak False
            test1 = abs((self._eVector[1] - self._sVector[1])*x - (self._eVector[0] - self._sVector[0])*y + self._eVector[0]*self._sVector[1] - self._eVector[1]*self._sVector[0])/sqrt((self._eVector[1] - self._sVector[1])**2 + (self._eVector[0] - self._sVector[0])**2)
            if not (test1 < 3):
                return False
            #Test ci lezi bod kliknutia vo stvoruholniku minx - 3 - maxx + 3; miny - 3 maxy +3
            minX = min(self._sVector[0], self._eVector[0])
            minY = min(self._sVector[1], self._eVector[1])
            test2 = (minX - 3 < x < (self._sVector[0] if minX == self._eVector[0] else self._eVector[0]) + 3) and (minY - 3 < y < (self._sVector[1] if minY == self._eVector[1] else self._eVector[1]) + 3)
            if test2:
                return True
            return False

    # Pridaj dieta kosti
    def AddChild(self, bone):
        self._children.append(bone)

    # Vypoctaj koncovy vektor kosti na zaklada uhla a dlzky a prveho vektora
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

    def __iter__(self):
        seq = ['id','x', 'y', 'length', 'angle']
        val = [self._id, self._sVector[0], self._sVector[1], self._lenght, self._angle]
        if self._parent != None:
            seq.append('parent_id')
            val.append(self._parent._id)

        for i in range(len(seq)):
            yield (seq[i], '{}'.format(val[i]))
