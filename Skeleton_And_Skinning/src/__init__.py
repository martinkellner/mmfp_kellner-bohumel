import wx

from src.gui.gui_Parent import Gui_Parent
from src.skeleton.skeleton import Skeleton

# Spustenie aplikacie, volanie inicializacie grafickeho rozhrania
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Gui_Parent(None, -1, "Skin and Bone", wx.DisplaySize())
    frame.Show()
    app.MainLoop()

