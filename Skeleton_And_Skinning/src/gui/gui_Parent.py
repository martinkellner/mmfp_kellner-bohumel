import sys
import wx

from os import path as ph
from src.gui.gui_surface import *
# Najvyssia cast GUI, tlacidla, menu, ...
class Gui_Parent(wx.Frame):

    def __init__(self, parent, ID, title, game_size):
        self._drawing = True        # True, ak je zapnute kreslenie kosti, inak False
        self._moving = False        # True, ak je zapnuty pohyb kosti, inak False
        self._skinning = False      # True, ak je zapnute editovanie skin-u, inak False

        # Nastavenie rozmerov aplikacie
        width, height = game_size
        wx.Frame.__init__(self, parent, ID, title, size=(width + 39, height + 34))

        # Menu bar
        menubar = wx.MenuBar()
        # Menu pre tlacidlo: save, open, quit
        fileMenu = wx.Menu()

        # Pridanie Save tlacidla do menu
        save_item = wx.MenuItem(fileMenu, wx.ID_SAVE, text='Save', kind=wx.ITEM_NORMAL)
        save_item.SetBitmap(wx.Bitmap(ph.join(sys.path[1], 'src\images\save_menu.png')))
        fileMenu.Append(save_item)

        #Pridanie Open tlacidla do menu
        open_item = wx.MenuItem(fileMenu, wx.ID_OPEN, text='Open', kind=wx.ITEM_NORMAL)
        open_item.SetBitmap(wx.Bitmap(ph.join(sys.path[1], 'src\images\open_menu.png')))
        fileMenu.Append(open_item)

        #Separator v menu
        fileMenu.AppendSeparator()

        # Pridanie tlacidla Quit v menu
        quit_item = wx.MenuItem(fileMenu, wx.ID_EXIT, text='Quit', kind=wx.ITEM_NORMAL)
        quit_item.SetBitmap(wx.Bitmap(ph.join(sys.path[1], 'src\images\quit_menu.png')))
        fileMenu.Append(quit_item)

        # Pridanie menu file fo menu bar
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Odchytavanie stlacenia tlacidla quit v menu file
        self.Bind(wx.EVT_MENU, self.OnQuit, quit_item)
        # Odchytavanie stlacenia tlacidla save v menu file
        self.Bind(wx.EVT_MENU, self.OnSave, save_item)
        # Odchytavanie stlacenia tlacidla open v menu file
        self.Bind(wx.EVT_MENU, self.OnOpen, open_item)

        # Inicializacie tool baru pre tlacidla
        self.surface_gui = Gui_Surface(self, -1, game_size)
        toolbar = self.CreateToolBar(style=wx.TB_VERTICAL | wx.TB_TEXT | wx.NO_BORDER | wx.TB_FLAT)

        # Pridanie tlacidle Edit (ak zapnute, tak mozes editovat kosti)
        self.id_drawing_tool = 2001
        toolbar.AddRadioTool(self.id_drawing_tool, '', wx.Bitmap(ph.join(sys.path[1], 'src\images\edit.png')), shortHelp="Edit")
        wx.EvtHandler.Bind(toolbar,event=wx.EVT_TOOL, handler=self.OnDrawingTool, id=self.id_drawing_tool)

        # Pridanie tlacidle Move (ak zapnute, tak mozes hybat kostami)
        self.id_moving_tool = 2002
        toolbar.AddRadioTool(self.id_moving_tool, '', wx.Bitmap(ph.join(sys.path[1], 'src\images\move.png')), shortHelp='Move')
        wx.EvtHandler.Bind(toolbar, event=wx.EVT_TOOL, handler=self.OnMovingTool, id=self.id_moving_tool)

        # Pridanie tlacidle Skinning (ak zapnute, tak mozes editovat skin)
        self.id_skinning_tool = 2003
        toolbar.AddRadioTool(self.id_skinning_tool, '', wx.Bitmap(ph.join(sys.path[1], 'src\images\mesh.png')), shortHelp="Skinning")
        wx.EvtHandler.Bind(toolbar, event=wx.EVT_TOOL, handler=self.OnSkinningTool, id=self.id_skinning_tool)

        toolbar.Realize()

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    # Odchytenie akcie stlacenia tlacidla na ukoncenie aplikacie
    def OnCloseWindow(self, event):
        self.surface_gui.pygame_surface_gui.Stop()
        self.Destroy()

    # Ak sa stlaci v toolbare tlacidlo pre kreslenie
    def OnDrawingTool(self, e):
        """Tool Draw pressed"""
        self._skinning = self._moving = False
        self._drawing = True

    # Ak sa stlaci v toolbare tlacidlo pre pohyb kosti
    def OnMovingTool(self, e):
        """Tool Move pressed"""
        self._drawing = self._moving = False
        self._moving = True

    # Ak sa stlaci v toolbare tlacidlo pre editaciu skin-u
    def OnSkinningTool(self, e):
        """Tool Skinning pressed"""
        self._drawing = self._moving = False
        self._skinning = True

    # Poskytni informaciu, ci je zapnuty tool kreslenie kosti
    def GetDrawing(self) -> bool:
        return self._drawing

    # Poskytni informaciu, ci je zapnuty tool pohyb kosti
    def GetMoving(self) -> bool:
        return self._moving

    # Poskytni informaciu, ci je zapnuty tool editacia skin-u
    def GetSkinning(self) -> bool:
        return self._skinning

    # Odchytenie akcie kliknutia na Quit v menu File -> ukonci aplikaciu
    def OnQuit(self, e):
        self.surface_gui.pygame_surface_gui.Stop()
        self.Close()

    # Odchytenie akcie kliknutia na Save v menu File -> z aktualneho skeletonu vytvor JSOn subor a uloz ho do
    # subory vybraneho pomocou dialogoveho okna
    def OnSave(self, e):
        with wx.FileDialog(self, "Save JSON file", wildcard="JSON files (*.json)|*.json",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    self.surface_gui.pygame_surface_gui.Instance_Skeleton().DoSaveData(file)
            except IOError:
                wx.LogError("Cannot save current data in file '%s'." % pathname)

    # Odchytenie akcie kliknutia na Open v menu File -> zo suboru zvoleneho pomocou dialogoveho okna nacitaj skeleton a nahrat to aktualnym
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
                    self.surface_gui.pygame_surface_gui.Instance_Skeleton().DoLoadFile(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % file)