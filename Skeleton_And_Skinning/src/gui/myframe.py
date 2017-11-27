import wx
from src.gui.sdlpanel import SDLPanel

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title, game_size):
        width, height = game_size
        wx.Frame.__init__(self, parent, ID, title, size=(width + 39, height + 34))
        self.pnlSDL = SDLPanel(self, -1, game_size)

        toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_TEXT | wx.NO_BORDER | wx.TB_FLAT)

        id_start = 2001
        #toolbar.AddLabelTool(id_start, label='Start', bitmap=wx.Bitmap('start.png'), shortHelp='Start Simulation')
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
