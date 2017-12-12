import pygame
import math

from src.bone import Bone

class Skeleton:

    def __init__(self):
        pygame.init()
        self._bones = []
        self._root = None
        self.OnlyDrawBone = None

    def OnHover(self, X, Y):
        for bone in self._bones:
            if  bone.IsOnHover(X, Y):
                bone.DrawEndPoints()
                return bone
            else:
                bone.RemoveEndPoints()
        return None

    def Redraw(self):
        if self.OnlyDrawBone:
            self.OnlyDrawBone.Draw()
        for bone in self._bones:
            bone.Draw()

    def AddBone(self, screen, sVector, eVector,  bone = None):
        cLength = math.sqrt((sVector[0] - eVector[0]) ** 2 + (sVector[1] - eVector[1]) ** 2)
        xDelta = eVector[0] - sVector[0]
        yDelta = eVector[1] - sVector[1]
        radian = math.atan2(yDelta, xDelta)
        if bone == None:
            if self._root == None:
                self._bones.append(Bone(screen, cLength, radian, sVector, None))
                self._root = self._bones[-1]
        else:
            self._bones.append(Bone(screen, cLength, radian, None, bone))


    def DrawOnly(self, screen, sVector, eVector, bone = None):
        cLength = math.sqrt((sVector[0] - eVector[0]) ** 2 + (sVector[1] - eVector[1]) ** 2)
        xDelta = eVector[0] - sVector[0]
        yDelta = eVector[1] - sVector[1]
        radian = math.atan2(yDelta, xDelta)
        if bone == None:
            b = Bone(screen, cLength, radian, sVector)
        else:
            b = Bone(screen, cLength, radian, parent=bone)
        self.OnlyDrawBone = b
