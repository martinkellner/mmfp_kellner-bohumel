import pygame
import math
import numpy as np
from numpy import arccos, array, dot, pi

from numpy.linalg import det, norm


class M_Vertex:

    def __init__(self, pVector):
        self._pVector = pVector
        self._weights = []
        self._infBones = []
        self._maxDist = 25.0;

    def Draw(self, screen):
        pygame.draw.circle(screen, pygame.Color('purple'),[int(self._pVector[0]), int(self._pVector[1])], 3, 0)

    def Tranformation(self):
        np_PVector = np.array([0.0, 0.0, 0.0])
        for i in range(len(self._infBones)):
            np_PVector += (np.dot(self._infBones[i].getWMatrix(), self._pVector) *  self._weights[i])
        print(np_PVector)
        self._pVector = np_PVector.tolist()

    def calInfBoneAndWeights(self, bones):
        distBones = []
        self._weights = []
        self._infBones = []
        for _bone in bones:
            bDistance = self.DistancePointLine(self._pVector[0], self._pVector[1], _bone._sVector[0],_bone._sVector[1], _bone._eVector[0], _bone._eVector[1])
            if self._maxDist < bDistance:
                continue
            distBones.append(bDistance)
            self._infBones.append(_bone)

        sDistances = sum(distBones)
        if len(distBones) == 0:
            self._infBones = []
            return
        elif len(distBones) == 1:
            self._weights.append(1)
            return
        for iDist in distBones:
            self._weights.append(1 - (iDist/sDistances))

    def lineMagnitude(self, x1, y1, x2, y2):
        lineMagnitude = math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))
        return lineMagnitude

    def DistancePointLine(self, px, py, x1, y1, x2, y2):
        # http://local.wasp.uwa.edu.au/~pbourke/geometry/pointline/source.vba
        LineMag = self.lineMagnitude(x1, y1, x2, y2)

        if LineMag < 0.00000001:
            DistancePointLine = 9999
            return DistancePointLine

        u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
        u = u1 / (LineMag * LineMag)

        if (u < 0.00001) or (u > 1):
            # // closest point does not fall within the line segment, take the shorter distance
            # // to an endpoint
            ix = self.lineMagnitude(px, py, x1, y1)
            iy = self.lineMagnitude(px, py, x2, y2)
            if ix > iy:
                DistancePointLine = iy
            else:
                DistancePointLine = ix
        else:
            # Intersecting point is on the line, use the formula
            ix = x1 + u * (x2 - x1)
            iy = y1 + u * (y2 - y1)
            DistancePointLine = self.lineMagnitude(px, py, ix, iy)

        return DistancePointLine
