import _thread as thread
import pygame as pyGame
from pygame import Color
from src.bone import Bone
from src.skeleton import Skeleton
import math
import random

xpos = None
ypos = None

class SDLThread(object):
    def __init__(self, screen):
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.surface = pyGame.display.get_surface()
        self.rect = self.surface.get_rect()
        self.screen.fill(Color('white'))
        self.bone = None
        self.skeleton = Skeleton()

    def Start(self):
        self.m_bKeepGoing = self.m_bRunning = True
        thread.start_new_thread(self.Run, ())

    def Stop(self):
        self.m_bKeepGoing = False

    def IsRunning(self):
        return self.m_bRunning

    def Run(self):
        self.setup()
        while self.m_bKeepGoing:
            if pyGame:
                self.update()
        self.m_bRunning = False;

    def setup(self):
        self.color = (255, 255, 255)
        self.r = (10, 10, 100, 100)

    def update(self):
        e = pyGame.event.poll()
        if e.type == pyGame.MOUSEBUTTONDOWN:
            self.color = (255, 0, 128)
            global xpos
            global ypos
            if xpos == None:
                xpos = (e.pos[0], e.pos[1])
            elif ypos == None:
                ypos = (e.pos[0], e.pos[1])
            if ypos != None and xpos != None:
                self.skeleton.addAndDraw(self.screen,xpos, ypos)
                xpos = ypos = None

        if e.type == pyGame.MOUSEMOTION:
            self.redraw()
            self.skeleton.checkBoneOnHover(e.pos[0], e.pos[1])

    def redraw(self):
        self.screen.fill(Color('white'))
        self.skeleton.redraw()