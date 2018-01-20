import _thread as thread
import pygame as pyGame
from pygame import Color
from src.skeleton.skeleton import *

# Cast GUI, akcie v grafickej ploche kniznice pyGame
# Vykreslovanie, tahanie objektov, atd.
class PyGame_Surface():

    #Konstruktor
    def __init__(self, wx_gui, screen):
        self.wx_gui = wx_gui                            # Referencia na druhu cast gui (tlacidla, menu, ...)
        self.m_bKeepGoing = self.m_bRunning = False
        self.screen = screen                            # Graficka plocha, vytvorena v inej casti gui
        ### Inicializacia grafickej plochy kniznice pyGame ###
        self.surface = pyGame.display.get_surface()     ######
        self.rect = self.surface.get_rect()          #########
        self.screen.fill(Color('white'))         #############

        ### Vytvorenie objekty Skeleton
        self.skeleton = Skeleton()
        ### Inizializacia premennej screen pre skeleton
        self.skeleton._screen = self.screen
        ##### Pomocne premenne pre pracu so skeletonom a skinnigom ###
        self.sVector = None         # Pomocna premenna - pociatocneho bodu kosti
        self.eVector = None         # Pomocna premenna - koncoveho bodu kosti
        self.bone = None            # Pomocna premenna
        self.boneSelected = None    # Pomocna premenna - vybrana na manipulaciu
        self.boneDragged = None     # Pomocna premenna - kost, ktora je tahana (hybe sa s nou, forward kinematic)
        self.boneExtending = False  # Pomocna premenna - True, ak sa kosti este urcuje koncovy bod, inak False
        self.mVectorHovered = None  # Pomocna premenna - Bod skinningu, na ktory sa ukazuje mysou
        self.mVectorSelected = None # Pomocna premenna - Bod skinningu, ktory je vybrani na manipulaciu

    # Odstatovanie odchytavania akcii v grafickej ploche
    def Start(self):
        self.m_bKeepGoing = self.m_bRunning = True
        thread.start_new_thread(self.Run, ())

    # Stopnutie cinnosti grafickej plochy, pri ukonceni aplikacie
    def Stop(self):
        self.m_bKeepGoing = False

    # True, ak bezi graficka plocha, inak False
    def IsRunning(self):
        return self.m_bRunning

    # Beh plochy
    def Run(self):
        self.setup()                # Nastavenie na bielu plochu
        while self.m_bKeepGoing:
            if pyGame:
                self.update()       # Odchytenie udalosti
                self.Redraw()       # Prekreslenie objektov
        self.m_bRunning = False

    # Prvotne nastavenie plochy
    def setup(self):
        self.color = (255, 255, 255)
        self.r = (10, 10, 100, 100)

    # Odchytavanie udalosti
    def update(self):
        e = pyGame.event.poll()
        # Odchytanie udalosti, ak bolo stlacene tlacidlo mysi
        if e.type == pyGame.MOUSEBUTTONDOWN:
            # Odchytanie udalosti, ak bolo stlacene prave tlacidlo mysi
            if e.button == 3:
                if self.wx_gui.GetDrawing():
                    self.RightBMouseDrawing()
                elif self.wx_gui.GetSkinning():
                    self.RightBMouseSkinning(e)
            # Odchytanie udalosti, ak bolo stlacene lave tlacidlo mysi
            else:
                if self.wx_gui.GetMoving():
                    self.LeftBMouseMoving()
                elif self.wx_gui.GetDrawing():
                    self.LeftBMouseDrawing(e)
                elif self.wx_gui.GetSkinning():
                    self.LeftBMouseSkinning(e)
        # Odchytanie udalosti pri pohybe mysou
        if e.type == pyGame.MOUSEMOTION:
            if self.wx_gui.GetDrawing():
                self.MoveMouseDrawing(e)
            elif self.wx_gui.GetMoving():
                self.MoveMouseMoving(e)
            elif self.wx_gui.GetSkinning():
                self.MoveMouseSkinning(e)
        # Odchytavanie udalosti stlacenia tlacidla DELETE
        if e.type == pyGame.KEYDOWN:
            '''key delete pressed'''
            if e.key == pyGame.K_DELETE:
                if self.boneSelected != None:
                    self.DeleteBone()
                elif self.mVectorSelected != None:
                    self.DeleteMVector()

    # Prekreslenie grafickej plochy, tj. objektov skin-u a skeletonu
    def Redraw(self):
        self.screen.fill(Color('white'))
        self.skeleton.DrawMesh(self.screen)
        self.skeleton.Redraw()
        pyGame.display.update()

    # Akcie pri pohybe mysou, ked je zapnute kreslenie kosti
    def MoveMouseDrawing(self, e):
        if not self.boneExtending and self.boneSelected == None:
            self.bone = self.skeleton.OnHoverBone(e.pos[0], e.pos[1])
        if self.sVector != None:
            self.skeleton.DrawOnly(self.screen, [self.sVector[0], self.sVector[1]], [e.pos[0], e.pos[1]], None)
        else:
            if self.bone and self.boneExtending:
                self.skeleton.DrawOnly(self.screen, self.bone._eVector, [e.pos[0], e.pos[1]], self.bone)

    # Akcie pri pohybe mysou, ked je zapnute hybanie skeletonom
    def MoveMouseMoving(self, e):
        if self.boneDragged != None:
            self.boneDragged.Move([e.pos[0], e.pos[1]])
            self.skeleton.TranformSkin()
            self.boneDragged._dAngle = 0
            self.boneDragged.RecalculateWorldMatrix()
            for _ch in self.boneDragged._children:
                _ch.RecalculateWorldMatrix()
        else:
            self.bone = self.skeleton.OnHoverBone(e.pos[0], e.pos[1])

    # Akcie pri stlaceni praveho tlacidla mysi, ked je zapnute kreslenie kosti
    def RightBMouseDrawing(self):
        if self.boneExtending:
            self.bone = self.sVector = self.eVector = None
            self.boneExtending = False
            self.skeleton.OnlyDrawBone = None
        elif self.boneSelected != None:
            self.boneSelected._selected = False
            self.boneSelected = None
        elif self.bone != None:
            self.boneSelected = self.bone
            self.boneSelected._selected = True

    # Akcie pri stlaceni laveho tlacidla mysi, ked je zapnuty pohyb kosti
    def LeftBMouseMoving(self):
        if self.boneDragged != None:
            self.boneDragged = None
            self.skeleton.RecalculateBoneWMatrix()
        elif self.bone != None:
            self.boneDragged = self.bone
            self.skeleton.OnlyDrawBone = None

    # Akcie pri stlaceni laveho tlacidla mysi, ked je zapnute kreslenie kosti
    def LeftBMouseDrawing(self, e):
        if self.boneSelected != None:
            self.boneSelected._selected = False
            self.boneSelected = None
        elif not self.boneExtending and self.bone != None:
            self.boneExtending = True
            self.bone._selected = True
        elif self.boneExtending and self.bone != None:
            self.skeleton.AddBone(self.screen, self.bone._eVector, [e.pos[0], e.pos[1], 1], self.bone)
            self.boneExtending = False
            self.bone._selected = False
            self.bone = None
        else:
            if self.sVector == None:
                self.sVector = (e.pos[0], e.pos[1], 1)
            elif self.eVector == None:
                self.eVector = (e.pos[0], e.pos[1], 1)
            if self.eVector != None and self.sVector != None:
                self.skeleton.AddBone(self.screen, self.sVector, self.eVector)
                self.sVector = self.eVector = None

    # Akcie pri stlaceni laveho tlacidla mysi, ked je zapnute editovanie skinnigu pre skeleton
    def LeftBMouseSkinning(self, e):
        if self.mVectorSelected != None:
            self.mVectorSelected._selected = False
            self.skeleton.RecalculateMVectorWeights(self.mVectorSelected)
            self.skeleton.RefreshSkinning()
            self.mVectorSelected = None
        else:
            self.skeleton.AddM_Vertex([e.pos[0], e.pos[1]])

    # Akcie pri pohybe mysi, ked je zapnuta editacia skinnugu
    def MoveMouseSkinning(self, e):
        if self.mVectorSelected == None:
            self.mVectorHovered = self.skeleton.OnHoverMVector(e.pos[0], e.pos[1])
        else:
            self.mVectorSelected.Drag([e.pos[0], e.pos[1]])

    # Akcie pri stlaceni praveho tlacidla mysi, ked je zapnuta editacia skinnigu
    def RightBMouseSkinning(self, e):
        if self.mVectorSelected != None:
            self.mVectorSelected._selected = False
            self.skeleton.RecalculateMVectorWeights(self.mVectorSelected)
            self.skeleton.RefreshSkinning()
            self.mVectorSelected = None
        elif self.mVectorHovered != None:
            self.mVectorSelected = self.mVectorHovered

    # Akcia pre mazanie vektorov skinning-u
    def DeleteMVector(self):
        if self.mVectorSelected != None:
            self.skeleton.DeleteMVector(self.mVectorSelected)
            self.mVectorSelected = None

    # Akcia pre mazanie kosti
    def DeleteBone(self):
        self.skeleton.DeleteBone(self.boneSelected)
        self.skeleton.OnlyDrawBone = None
        self.boneSelected = None

    # Odovzdanie instancie objektu skeletonu pre ine triedy
    def Instance_Skeleton(self):
        return self.skeleton