import wx
import pygame as pyGame
import _thread as thread
import os
from src.gui.sdlthread import SDLThread

class SDLPanel(wx.Panel):
    def __init__(self, parent, ID, game_size):
        global pyGame
        wx.Panel.__init__(self, parent, ID, size=game_size)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame
        pyGame = pygame
        pyGame.display.init()
        window = pyGame.display.set_mode(game_size)
        self.thread = SDLThread(window)
        self.thread.Start()
