import _thread as thread
import pygame as pyGame
from pygame import Color
from src.bone import Bone
from src.skeleton import Skeleton

class SDLThread(object):
    def __init__(self, screen):
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.surface = pyGame.display.get_surface()
        self.rect = self.surface.get_rect()
        self.screen.fill(Color('white'))
        self.sk = Skeleton(self.screen)


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
            self.r = (e.pos[0], e.pos[1], 100, 100)

