import wx
import os.path as ph
import sys
from src.gui.sdlpanel import SDLPanel

class MyFrame(wx.Frame):

    def __init__(self, parent, ID, title, game_size):
        self.editing = False

        width, height = game_size
        wx.Frame.__init__(self, parent, ID, title, size=(width + 39, height + 34))
        self.pnlSDL = SDLPanel(self, -1, game_size)

        toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_TEXT | wx.NO_BORDER | wx.TB_FLAT)

        id_start = 2001
        print(ph.curdir)
        editToolbarCheckButton = toolbar.AddCheckTool(id_start, '' ,wx.Bitmap(ph.join(sys.path[1], 'resource\images\edit.png')), shortHelp="Edit")
        self.Bind(wx.EVT_LEFT_DCLICK, self.changeEditing(), editToolbarCheckButton)
        wx.EVT_TOOL(self, id_start, self.OnStartSimulation)


        id_stop = 2002
        #toolbar.AddLabelTool(id_stop, label='Stop', bitmap=wx.Bitmap('stop.png'), shortHelp='Stop Simulation')
        wx.EVT_TOOL(self, id_stop, self.OnStopSimulation)

        id_quit = 2003
        #toolbar.AddLabelTool(id_quit, label='Quit', bitmap=wx.Bitmap('quit.png'), shortHelp='Quit Simulation')
        wx.EVT_TOOL(self, id_quit, self.OnCloseWindow)

        toolbar.Realize()

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnStartSimulation(self, event):
        """Start button pressed"""
        print
        'Start', event

    def OnStopSimulation(self, event):
        """Stop button pressed"""
        print
        'Stop', event

    def OnSize(self, event):
        size = self.GetClientSize()
        print
        'resizing', size
        if getattr(self, 'app', None):
            self.app.update()
        event.Skip()

    def OnCloseWindow(self, event):
        self.Destroy()

    def changeEditing(self):
        #TODO: set self.editing to allow draw a skeleton
        pass

