import pygame
import math

from pygame import Color
from setuptools.command.saveopts import saveopts

from src.bone import Bone
from src.gui import sdlthread

class Skeleton:

    def __init__(self):
        pygame.init()
        self._bones = []

    def addBone(self, bone):
        self._bones.append(bone)

    def addRootBone(self, bone):
        pass

    def checkBoneOnHover(self, sx, ex):
        for bone in self._bones:
            bone.isOnHover(sx, ex)
            if  bone.isOnHover(sx, ex):
                bone.drawEndPoints()
                pygame.display.update()
                return bone
            else:
                bone.removeEndPoints()
            pygame.display.update()
        return None

    def redraw(self):
        for bone in self._bones:
            bone.draw()

    def addAndDraw(self, screen, xpos, ypos,  bone = None):
        cLength = math.sqrt((xpos[0] - ypos[0]) ** 2 + (xpos[1] - ypos[1]) ** 2)
        xDelta = ypos[0] - xpos[0]
        yDelta = ypos[1] - xpos[1]
        radian = math.atan2(yDelta, xDelta)
        angle = radian * (180 / math.pi)
        if bone == None:
            self._bones.append(Bone(screen, True, cLength, angle, xpos[0], xpos[1], None))
        else:
            self._bones.append(Bone(screen, False, cLength, angle, ypos[0], ypos[1], bone))

    def drawOnly(self, screen, xpos, ypos, bone = None):
        cLength = math.sqrt((xpos[0] - ypos[0]) ** 2 + (xpos[1] - ypos[1]) ** 2)
        xDelta = ypos[0] - xpos[0]
        yDelta = ypos[1] - xpos[1]
        radian = math.atan2(yDelta, xDelta)
        angle = radian * (180 / math.pi)
        b = None
        if bone == None:
            b = Bone(screen, True, cLength, angle, xpos[0], xpos[1], None)
        else:
            b = Bone(screen, False, cLength, angle, ypos[0], ypos[1], bone)
        b.draw()
        pygame.display.update();
