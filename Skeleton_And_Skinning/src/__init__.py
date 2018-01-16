import wx

from src.gui.myframe import MyFrame
from src.skeleton.skeleton import Skeleton

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MyFrame(None, -1, "Skin and Bone", (1024, 576))
    frame.Show()
    app.MainLoop()

