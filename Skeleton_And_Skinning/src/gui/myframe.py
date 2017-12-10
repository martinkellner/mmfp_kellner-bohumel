import wx
import os.path as ph
import sys
from src.gui.sdlpanel import SDLPanel

class MyFrame(wx.Frame):

    def __init__(self, parent, ID, title, game_size):
        self._drawing = False

        width, height = game_size
        wx.Frame.__init__(self, parent, ID, title, size=(width + 39, height + 34))

        self.pnlSDL = SDLPanel(self, -1, game_size)
        toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_TEXT | wx.NO_BORDER | wx.TB_FLAT)

        id_drawing_tool = 2001
        toolbar.AddCheckTool(id_drawing_tool, '' ,wx.Bitmap(ph.join(sys.path[1], 'resource\images\edit.png')), shortHelp="Edit")
        wx.EvtHandler.Bind(toolbar,event=wx.EVT_TOOL, handler=self.OnDrawingTool, id=id_drawing_tool)

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

    def OnDrawingTool(self, e):
        """Tool Draw pressed"""
        self._drawing = not self._drawing

    def OnKeyDown(self, e):
        """Any key pressed"""
        print(e)

    def GetDrawing(self) -> bool:
        return self._drawing

