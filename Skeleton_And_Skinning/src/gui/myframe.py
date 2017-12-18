import wx
import os.path as ph
import sys
from src.gui.sdlpanel import SDLPanel

class MyFrame(wx.Frame):

    def __init__(self, parent, ID, title, game_size):
        self._drawing = True
        self._moving = False
        self._skinning = False

        width, height = game_size
        wx.Frame.__init__(self, parent, ID, title, size=(width + 39, height + 34))

        self.pnlSDL = SDLPanel(self, -1, game_size)
        toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_TEXT | wx.NO_BORDER | wx.TB_FLAT)

        self.id_drawing_tool = 2001
        toolbar.AddRadioTool(self.id_drawing_tool, '' ,wx.Bitmap(ph.join(sys.path[1], 'resource\images\edit.png')), shortHelp="Edit")
        wx.EvtHandler.Bind(toolbar,event=wx.EVT_TOOL, handler=self.OnDrawingTool, id=self.id_drawing_tool)

        self.id_moving_tool = 2002
        toolbar.AddRadioTool(self.id_moving_tool, '', wx.Bitmap(ph.join(sys.path[1], 'resource\images\move.png')), shortHelp="Move")
        wx.EvtHandler.Bind(toolbar, event=wx.EVT_TOOL, handler=self.OnMovingTool, id=self.id_moving_tool)

        self.id_skinning_tool = 2003
        toolbar.AddRadioTool(self.id_skinning_tool, '', wx.Bitmap(ph.join(sys.path[1], 'resource\images\mesh.png')),
                             shortHelp="Skinning")
        wx.EvtHandler.Bind(toolbar, event=wx.EVT_TOOL, handler=self.OnSkinningTool, id=self.id_skinning_tool)

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
        self._skinning = self._moving = False
        self._drawing = True

    def OnMovingTool(self, e):
        """Tool Move pressed"""
        self._drawing = self._moving = False
        self._moving = True

    def OnSkinningTool(self, e):
        """Tool Skinning pressed"""
        self._drawing = self._moving = False
        self._skinning = True

    def OnKeyDown(self, e):
        """Any key pressed"""
        print(e)

    def GetDrawing(self) -> bool:
        return self._drawing

    def GetMoving(self) -> bool:
        return self._moving

    def GetSkinning(self) -> bool:
        return self._skinning
