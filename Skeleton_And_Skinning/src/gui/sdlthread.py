import _thread as thread
import pygame as pyGame
from pygame import Color
from src.skeleton.skeleton import *

sVector = None
eVector = None
bone = None
boneSelected = None
dragBone = None
extendLine = False
mVectorHovered = None
mVectorSelected = None

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
        self.skeleton._screen = self.screen

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
        e = pyGame.event.poll()

        if e.type == pyGame.MOUSEBUTTONDOWN:
            if e.button == 3:
                if self._parent.GetDrawing():
                    self.DrawingBoneRMouseDown()
                elif self._parent.GetSkinning():
                    self.SkinningRMouseDown(e)
            else:
                if self._parent.GetMoving():
                    self.MovingLMouseDown()
                elif self._parent.GetDrawing():
                    self.DragingLMouseDown(e)
                elif self._parent.GetSkinning():
                    self.SkinningLMouseDown(e)

        if e.type == pyGame.MOUSEMOTION:
            if self._parent.GetDrawing():
                self.DrawingBoneMMouse(e)
            elif self._parent.GetMoving():
                self.MovingBoneMMouse(e)
            elif self._parent.GetSkinning():
                self.SkinningMMouse(e)

        if e.type == pyGame.KEYDOWN:
            '''key delete pressed'''
            if e.key == pyGame.K_DELETE:
                if boneSelected != None:
                    self.DeleteBone()
                elif mVectorSelected != None:
                    self.DeleteMVector()

    def Redraw(self):
        self.screen.fill(Color('white'))
        self.skeleton.DrawMesh(self.screen)
        self.skeleton.Redraw()
        pyGame.display.update()

    def DrawingBoneMMouse(self, e):
        global bone, boneSelected
        if not extendLine and boneSelected == None:
            bone = self.skeleton.OnHoverBone(e.pos[0], e.pos[1])
        if sVector != None:
            self.skeleton.DrawOnly(self.screen, [sVector[0], sVector[1]], [e.pos[0], e.pos[1]], None)
        else:
            if bone and extendLine:
                self.skeleton.DrawOnly(self.screen, bone._eVector, [e.pos[0], e.pos[1]], bone)

    def MovingBoneMMouse(self, e):
        global bone, dragBone
        if dragBone != None:
            dragBone.Move([e.pos[0], e.pos[1]])
            self.skeleton.TranformSkin()
            dragBone._dAngle = 0
            dragBone.ReCalwMatrix()
            for _ch in dragBone._children:
                _ch.ReCalwMatrix()
        else:
            bone = self.skeleton.OnHoverBone(e.pos[0], e.pos[1])

    def DrawingBoneRMouseDown(self):
        global bone, extendLine, sVector, eVector, boneSelected
        if extendLine:
            bone = sVector = eVector = None
            extendLine = False
            self.skeleton.OnlyDrawBone = None
        elif boneSelected != None:
            boneSelected._selected = False
            boneSelected = None
        elif bone != None:
            boneSelected = bone
            boneSelected._selected = True

    def MovingLMouseDown(self):
        global dragBone
        if dragBone != None:
            dragBone = None
            self.skeleton.RstWBnsWMatrix()
        elif bone != None:
            dragBone = bone
            self.skeleton.OnlyDrawBone = None

    def DragingLMouseDown(self, e):
        global extendLine, bone, sVector, eVector, boneSelected
        if boneSelected != None:
            boneSelected._selected = False
            boneSelected = None
        elif not extendLine and bone != None:
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
                self.skeleton.AddBone(self.screen, sVector, eVector)
                sVector = eVector = None

    def SkinningLMouseDown(self, e):
        global mVectorSelected
        if mVectorSelected != None:
            mVectorSelected._selected = False
            self.skeleton.CallReCalculateMVector(mVectorSelected)
            self.skeleton.RefreshSkinning()
            mVectorSelected = None
        else:
            self.skeleton.AddM_Vertex([e.pos[0], e.pos[1]])

    def DeleteBone(self):
        global boneSelected
        self.skeleton.DeleteBone(boneSelected)
        self.skeleton.OnlyDrawBone = None
        boneSelected = None

    def SkinningMMouse(self, e):
        global mVectorHovered, mVectorSelected
        if mVectorSelected == None:
            mVectorHovered = self.skeleton.OnHoverMVector(e.pos[0], e.pos[1])
        else:
            mVectorSelected.Drag([e.pos[0], e.pos[1]])

    def SkinningRMouseDown(self, e):
        global mVectorHovered, mVectorSelected
        if mVectorSelected != None:
            mVectorSelected._selected = False
            self.skeleton.CallReCalculateMVector(mVectorSelected)
            self.skeleton.RefreshSkinning()
            mVectorSelected = None
        elif mVectorHovered != None:
            mVectorSelected = mVectorHovered

    def DeleteMVector(self):
        global mVectorSelected
        if mVectorSelected != None:
            self.skeleton.DeleteMVector(mVectorSelected)
            mVectorSelected = None

    def Instance_Skeleton(self):
        return self.skeleton