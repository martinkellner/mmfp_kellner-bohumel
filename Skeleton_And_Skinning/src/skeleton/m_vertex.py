import pygame
import math
import numpy as np

class M_Vertex:

    def __init__(self, pVector):
        self._pVector = pVector
        self._weights = []
        self._infBones = []
        self._maxDist = 30.0
        self._selected = False

    def Draw(self, screen):
        pygame.draw.circle(screen, pygame.Color('purple'),[int(self._pVector[0]), int(self._pVector[1])], 5 if self._selected else 3, 0)

    def Tranformation(self):
        np_PVector = np.array([0.0, 0.0, 0.0])
        old_PVector = self._pVector + [1]
        for i in range(len(self._infBones)):
            np_PVector += (np.dot(self._infBones[i]._wMatrix, old_PVector) *  self._weights[i])
        self._pVector[0] = round(np_PVector[0], 4)
        self._pVector[1] = round(np_PVector[1], 4)

    def CallInfBoneAndWeights(self, bones):
        distBones = []
        self._weights = []
        self._infBones = []
        for _bone in bones:
            bDistance = self.DistancePointLine(self._pVector[0], self._pVector[1], _bone._sVector[0],_bone._sVector[1], _bone._eVector[0], _bone._eVector[1])
            distBones.append(bDistance)
            self._infBones.append(_bone)

        #filtering bones with low influece on skin vector
        c_infBones = []
        c_distBones = []
        min_distance = min(distBones)
        for i in range(len(distBones)):
            if (min_distance * 1.1) > distBones[i]:
                c_distBones.append(distBones[i])
                c_infBones.append(self._infBones[i])
        self._infBones = c_infBones
        distBones = c_distBones
        sum_distance = sum(distBones)
        for i in distBones:
            self._weights.append((sum_distance-i)/sum_distance)
        if len(self._weights) == 1:
            self._weights = [1]
        else:
            sum_weights = sum(self._weights)
            self._weights = list(map(lambda x: x/sum_weights, self._weights))


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

    def ReCalculate(self, bones):
        self.CallInfBoneAndWeights(bones)
        self.Tranformation()

    def OnHover(self, x, y):
        return math.sqrt((x-self._pVector[0])**2 + (y-self._pVector[1])**2) < 5

    def Drag(self, nwPvector):
        self._pVector = nwPvector

    def __iter__(self):
        seq = ['x', 'y', 'inf_bones', 'weights']
        val = [self._pVector[0], self._pVector[1]] + [[ b._id for b in self._infBones ]] + [[ w for w in self._weights ]]

        for i in range(4):
            yield (seq[i], val[i])
