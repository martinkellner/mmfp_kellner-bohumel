import sys
import wx

from os import path as ph
from src.gui.sdlpanel import *

class MyFrame(wx.Frame):

    def __init__(self, parent, ID, title, game_size):
        self._drawing = True
        self._moving = False
        self._skinning = False

        width, height = game_size
        wx.Frame.__init__(self, parent, ID, title, size=(width + 39, height + 34))

        menubar = wx.MenuBar()
        fileMenu = wx.Menu()

        save_item = wx.MenuItem(fileMenu, wx.ID_SAVE, text='Save', kind=wx.ITEM_NORMAL)
        save_item.SetBitmap(wx.Bitmap(ph.join(sys.path[1], 'src\images\save_menu.png')))
        fileMenu.Append(save_item)

        open_item = wx.MenuItem(fileMenu, wx.ID_OPEN, text='Open', kind=wx.ITEM_NORMAL)
        open_item.SetBitmap(wx.Bitmap(ph.join(sys.path[1], 'src\images\open_menu.png')))
        fileMenu.Append(open_item)

        fileMenu.AppendSeparator()

        quit_item = wx.MenuItem(fileMenu, wx.ID_EXIT, text='Quit', kind=wx.ITEM_NORMAL)
        quit_item.SetBitmap(wx.Bitmap(ph.join(sys.path[1], 'src\images\quit_menu.png')))
        fileMenu.Append(quit_item)

        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)
        self.Bind(wx.EVT_MENU, self.OnSave, save_item)
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)

        self.pnlSDL = SDLPanel(self, -1, game_size)
        toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_TEXT | wx.NO_BORDER | wx.TB_FLAT)

        self.id_drawing_tool = 2001
        toolbar.AddRadioTool(self.id_drawing_tool, '', wx.Bitmap(ph.join(sys.path[1], 'src\images\edit.png')), shortHelp="Edit")
        wx.EvtHandler.Bind(toolbar,event=wx.EVT_TOOL, handler=self.OnDrawingTool, id=self.id_drawing_tool)

        self.id_moving_tool = 2002
        toolbar.AddRadioTool(self.id_moving_tool, '', wx.Bitmap(ph.join(sys.path[1], 'src\images\move.png')), shortHelp='Move')
        wx.EvtHandler.Bind(toolbar, event=wx.EVT_TOOL, handler=self.OnMovingTool, id=self.id_moving_tool)

        self.id_skinning_tool = 2003
        toolbar.AddRadioTool(self.id_skinning_tool, '', wx.Bitmap(ph.join(sys.path[1], 'src\images\mesh.png')), shortHelp="Skinning")
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
        pass

    def GetDrawing(self) -> bool:
        return self._drawing

    def GetMoving(self) -> bool:
        return self._moving

    def GetSkinning(self) -> bool:
        return self._skinning

    def OnQuit(self, e):
        self.Close()

    def OnSave(self, e):
        with wx.FileDialog(self, "Save JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.pnlSDL.thread.Instance_Skeleton().DoSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnOpen(self, e):
        #if self.contentNotSaved:
        #    if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
        #                     wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #        return
        # otherwise ask the user what new file to open

        with wx.FileDialog(self, "Open JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.pnlSDL.thread.Instance_Skeleton().DoLoadFile(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % file)