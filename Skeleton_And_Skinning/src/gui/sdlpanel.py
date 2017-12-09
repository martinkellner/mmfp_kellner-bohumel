import wx
import os
from src.gui.sdlthread import SDLThread

class SDLPanel(wx.Panel):

    def __init__(self, parent, ID, game_size):
        wx.Panel.__init__(self, parent, ID, size=game_size)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame
        pygame = pygame
        pygame.display.init()
        window = pygame.display.set_mode(game_size)
        self.thread = SDLThread(parent, window)
        self.thread.Start()

