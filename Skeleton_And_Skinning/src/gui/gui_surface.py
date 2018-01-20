import os
import wx

from src.gui.pyGame_Surface import *

# Medzi clanok pre spolupracu grafickej kniznice pyGame a wx.
# Do panelu wx je pridana plocha pyGame kniznice
class Gui_Surface(wx.Panel):

    def __init__(self, parent, ID, game_size):
        wx.Panel.__init__(self, parent, ID, size=game_size)
        self.Fit()
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame
        pygame = pygame
        pygame.display.init()
        window = pygame.display.set_mode(game_size)
        self.pygame_surface_gui = PyGame_Surface(parent, window)
        self.pygame_surface_gui.Start()
