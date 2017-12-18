import _thread as thread
import pygame as pyGame
from pygame import Color
from skeleton import Skeleton

sVector = None
eVector = None
bone = None
dragBone = None
extendLine = False

class SDLThread(object):

    def __init__(self, parent, screen):
        self._parent = parent
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen
        self.surface = pyGame.display.get_surface()
        self.surface.set_alpha(128)  # alpha level
        self.rect = self.surface.get_rect()
        self.screen.fill(Color('white'))
        self.bone = None
        self.boneHover = None
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
                self.Redraw()
        self.m_bRunning = False

    def setup(self):
        self.color = (255, 255, 255)
        self.r = (10, 10, 100, 100)

    def update(self):

        global bone, extendLine, boneHover, dragBone, sVector, eVector
        e = pyGame.event.poll()

        if e.type == pyGame.MOUSEBUTTONDOWN:
            if e.button == 3:
                if self._parent.GetDrawing():
                    bone = sVector = eVector = None
                    extendLine = False
                    self.skeleton.OnlyDrawBone = None
            else:
                if self._parent.GetMoving():
                    if dragBone != None:
                        dragBone = None
                        self.skeleton.RstWBnsWMatrix()
                    elif bone != None:
                        dragBone = bone
                        self.skeleton.OnlyDrawBone = None
                elif self._parent.GetDrawing():
                    if not extendLine and bone != None:
                        extendLine = True
                        bone._selected = True
                    elif extendLine and bone != None:
                        self.skeleton.AddBone(self.screen, bone._eVector, [e.pos[0], e.pos[1], 1], bone)
                        extendLine = False
                        bone._selected = False
                        bone = None
                    else:
                        if sVector == None:
                            sVector = (e.pos[0], e.pos[1], 1)
                        elif eVector == None:
                            eVector = (e.pos[0], e.pos[1], 1)
                        if eVector != None and sVector != None:
                            self.skeleton.AddBone(self.screen,sVector, eVector)
                            sVector = eVector = None

                elif self._parent.GetSkinning():
                    self.skeleton.AddM_Vertex([e.pos[0], e.pos[1]])

        if e.type == pyGame.MOUSEMOTION:
            if self._parent.GetDrawing():
                if not extendLine:
                    bone = self.skeleton.OnHover(e.pos[0], e.pos[1])
                if sVector != None:
                    self.skeleton.DrawOnly(self.screen, [sVector[0], sVector[1]], [e.pos[0], e.pos[1]], None)
                else:
                    if bone and extendLine:
                        self.skeleton.DrawOnly(self.screen, bone._eVector, [e.pos[0], e.pos[1]], bone)
            elif self._parent.GetMoving():
                if dragBone != None:
                    dragBone.Move([e.pos[0], e.pos[1]])
                    self.skeleton.TranformSkin()
                    dragBone._dAngle = 0
                    dragBone.ReCalwMatrix()
                    for _ch in dragBone._children:
                        _ch.ReCalwMatrix()
                else:
                    bone = self.skeleton.OnHover(e.pos[0], e.pos[1])

    def Redraw(self):
        self.screen.fill(Color('white'))
        self.skeleton.DrawMesh(self.screen)
        self.skeleton.Redraw()
        pyGame.display.update()







