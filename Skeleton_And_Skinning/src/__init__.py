import pygame
import wx
from src.gui.myframe import MyFrame
from src.skeleton import Skeleton

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(None, -1, "Danger Island", (1024, 576))
    frame.Show()
    app.MainLoop()

