import wx, os

print_debug = 0
file_name = ""
file_modified = False

def debug(text):
    if print_debug:
        print text

# (type, image par defaut, ennemi ?, brique ? [, ...])
actorTypes = { "Brick":("brick.gif", 0), "MadBrick":("bad_brick.gif", 0), "WeakBrick":("kcirb.gif", 0),
    "Pike":("capique2.gif", 0), "Life":("heart1.gif", 2), "Pizza":("piz1.gif", 2), "Pizzaman":("pizzaman.gif", 2),
    "Waddledee":("waddledee1.gif", 1), "Togezo":("togezo1.gif", 1), "Dafly":("dafly1.gif", 1) }
actorsId = {}

wildcard = "Pydza level (*.pdz)|*.pdz|All Files|*.*"

ID_TOOLS = 10001

def imopj(file):
    return os.path.join("img",file)

class Shape:
    def __init__(self, id, pos=(64,64)):
        self.id = id
        self.image = actorTypes[id][0]
        self.type = actorTypes[id][1]
        if self.type == 1:
            self.dir = 1
        bmp = wx.Image(imopj(self.image), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        self.bmp = bmp
        self.pos = pos
        self.shown = True
        self.fullscreen = False

    def HitTest(self, pt):
        rect = self.GetRect()
        return rect.InsideXY(pt.x, pt.y)

    def GetRect(self):
        return wx.Rect(self.pos[0], self.pos[1],
                      self.bmp.GetWidth(), self.bmp.GetHeight())

    def Draw(self, dc, op = wx.COPY):
        if self.bmp.Ok():
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.bmp)

            dc.Blit(self.pos[0], self.pos[1],
                    self.bmp.GetWidth(), self.bmp.GetHeight(),
                    memDC, 0, 0, op, True)
            return True
        else:
            return False

    def SetBitmap(self, imName):
            self.bmp = wx.Image(imopj(imName), wx.BITMAP_TYPE_GIF).ConvertToBitmap()
            self.image = imName

    def SetDirectionalBitmap(self, newDir):
        if newDir != self.dir:
            self.dir = newDir
            im = wx.Image(imopj(self.image), wx.BITMAP_TYPE_GIF)
            if newDir == 1:
                bmp = im.ConvertToBitmap()
            else:
                bmp = im.Mirror().ConvertToBitmap()
            self.bmp = bmp

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN
        wx.Frame.__init__(self, parent, -1, title, pos=(150, 150), size=(727, 608), style=style) #647,544

        # Create the menubar
        menuBar = wx.MenuBar()
        # and a menu 
        menuFile = wx.Menu()

        # add an item to the menu, using \tKeyName automatically
        # creates an accelerator, the third param is some help text
        # that will show up in the statusbar
        menuFile.Append(wx.ID_NEW, "&New\tCtrl-N", "Begin a new level")
        menuFile.Append(wx.ID_OPEN, "&Open\tCtrl-O", "Open an existing level")
        menuFile.Append(wx.ID_SAVE, "&Save\tCtrl-S", "Save current level")
        menuFile.Append(wx.ID_SAVEAS, "Save As...", "Save current level as...")
        menuFile.AppendSeparator()
        menuFile.Append(wx.ID_EXIT, "Quit")

        # bind the menu event to an event handler
        self.Bind(wx.EVT_MENU, self.OnMenuQuit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnMenuNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnMenuOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnMenuSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.OnMenuSaveAs, id=wx.ID_SAVEAS)

        self.menuTools = wx.Menu()
        self.menuTools.AppendCheckItem(ID_TOOLS, "Show Tools")
        self.menuTools.Check(ID_TOOLS, True)
        self.Bind(wx.EVT_MENU, self.OnToggleTools, id=ID_TOOLS)

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT, "About...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)

        # and put the menu on the menubar
        menuBar.Append(menuFile, "&File")
        menuBar.Append(self.menuTools, "&Tools")
        menuBar.Append(menuHelp, "&Help")
        self.SetMenuBar(menuBar)

        #self.CreateStatusBar(2,wx.FULL_REPAINT_ON_RESIZE)
        sb = CustomStatusBar(self, -1)
        self.SetStatusBar(sb)

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)

        self.level = LevelWindow(panel, -1)

        # and a few controls
        self.btnL = wx.Button(panel, -1, "<<", size=(28,25))
        self.btnL.SetPosition((5,240))
        self.btnL.Enable(False)
        btnR = wx.Button(panel, -1, ">>", size=(28,25))
        btnR.SetPosition((688,240))

        # bind the button events to handlers
        self.Bind(wx.EVT_BUTTON, self.level.OnMoveLeft, self.btnL)
        self.Bind(wx.EVT_BUTTON, self.level.OnMoveRight, btnR)
        self.Bind(wx.EVT_CLOSE, self.OnCloseMe)

        self.tools = ToolsWindow(self, -1)
        self.tools.Bind(wx.EVT_CLOSE, self.OnCloseTools)
        self.bShowTools = True
        self.tools.Show(True)

    def askToSave(self, action):
        global file_modified
        if not file_modified:
            return True

        response = wx.MessageBox("Save changes before " + action + "?",
                                "Confirm", wx.YES_NO | wx.CANCEL, self)
        if response == wx.YES:
            return self.OnMenuSave(None)
        elif response == wx.NO:
            return True # User doesn't want changes saved.
        elif response == wx.CANCEL:
            return False # User cancelled.

    def OnMenuNew(self, evt):
        global file_name, file_modified
        if not self.askToSave("creating a new level"):
            return
        debug("New")
        self.level.shapes = []
        self.level.levelPosition = 0
        self.btnL.Enable(False)
        self.level.Refresh()
        file_name = ""
        file_modified = False

    def OnMenuOpen(self, evt):
        global file_name
        debug("Open")

        if not self.askToSave("opening"):
            return

        dlg = wx.FileDialog(
            self, message="Choose a file", defaultDir="levels", 
            defaultFile="", wildcard=wildcard, style=wx.OPEN)# | wx.CHANGE_DIR)

        if dlg.ShowModal() == wx.ID_OK:
            file_name = dlg.GetPath()
            self.LoadLevel()

        dlg.Destroy()

    def OnMenuSave(self, evt):
        global file_name
        debug("Save")
        if file_name == "":
            return self.OnMenuSaveAs(evt)
        else:
            self.SaveLevel()
            return True

    def OnMenuSaveAs(self, evt):
        global file_name
        debug("Save as")
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir="levels", 
            defaultFile=file_name, wildcard=wildcard, style=wx.SAVE | wx.OVERWRITE_PROMPT)

        resul = dlg.ShowModal()
        if resul == wx.ID_OK:
            file_name = dlg.GetPath()
            self.SaveLevel()

        dlg.Destroy()
        return resul == wx.ID_OK

    def OnMenuQuit(self, evt):
        debug("Menu quit")
        self.Close()

    def OnAbout(self, evt):
        wx.MessageBox("Pydza Editor\n\nBy Alban 'spl0k' FERON\n\nhttp://pydza.sourceforge.net/", "About PydzEd",
            wx.OK, self)

    def OnCloseMe(self, evt):
        debug("OnCloseMe")
        if self.askToSave("closing"):
            self.Destroy()

    def OnToggleTools(self, evt):
        debug("Toggle tools window")
        self.bShowTools = not self.bShowTools
        self.tools.Show(self.bShowTools)

    def OnCloseTools(self, evt):
        debug("Closing tools")
        self.bShowTools = False
        self.tools.Show(False)
        self.menuTools.Check(ID_TOOLS, False)

    def OnToolClick(self, evt):
        global file_modified
        file_modified = True
        debug("Tool button %s" % evt.GetId())
        id = evt.GetId()
        if id == self.level.placingActorId:
            self.level.placingActorId = -1
            self.level.shapes.remove(self.level.placingActor)
            self.level.placingActor = None
        else:
            if self.level.placingActor is not None:
                self.level.shapes.remove(self.level.placingActor)
            self.level.placingActor = Shape(actorsId[id])
            self.level.shapes.append(self.level.placingActor)
            self.level.placingActorId = id
        self.level.Refresh()

    def OnGridSnap(self, evt):
        self.level.snap = evt.GetEventObject().GetValue()

    def SaveLevel(self):
        global file_modified
        if file_name == "":
            return

        debug("saving...")
        if self.level.placingActor is not None:
            self.level.shapes.remove(self.level.placingActor)
            self.level.placingActor = None
            self.level.placingActorId = -1
            self.level.Refresh() # mostly useless

        level = []
        ennemies = []
        maxlen = 0
        for shape in self.level.shapes:
            if shape.type == 1:
                ennemies.append(shape)
            else:
                level.append(shape)
            if shape.pos[0]+shape.bmp.GetWidth()+self.level.levelPosition > maxlen:
                maxlen = shape.pos[0]+shape.bmp.GetWidth()+self.level.levelPosition

        try:
            f = file(file_name, 'w')
            f.write("[level]\nsize:%d\n\n" % maxlen)
            for shape in level:
                f.write("%s:%d:%d" % (shape.id, shape.pos[0]+self.level.levelPosition, shape.pos[1]-64))
                if shape.type == 0:
                    f.write(":%s" % shape.image[:-4])
                f.write("\n")
            f.write("\n[ennemies]\n")
            for shape in ennemies:
                f.write("%s:%d:%d:%d\n" % (shape.id, shape.pos[0]+self.level.levelPosition, shape.pos[1]-64, shape.dir))
            f.close()
            file_modified = False
        except IOError:
            print 'Error while writing "%s"' % file_name

    def LoadLevel(self):
        global file_modified
        debug("opening...")
        file_modified = False

class CustomStatusBar(wx.StatusBar):
    def __init__(self, parent, id):
        wx.StatusBar.__init__(self, parent, id, style=wx.FULL_REPAINT_ON_RESIZE)
        self.SetFieldsCount(2)
        self.SetStatusWidths([550,-1])

        self.snapCB = wx.CheckBox(self, -1, "Snap to grid")
        self.snapCB.SetValue(True)
        self.Bind(wx.EVT_CHECKBOX, parent.OnGridSnap, self.snapCB)
        self.Reposition()

    def Reposition(self):
        rect = self.GetFieldRect(1)
        self.snapCB.SetPosition((rect.x+2, rect.y+2))
        self.snapCB.SetSize((rect.width-4, rect.height-4))

class LevelWindow(wx.Window):
    def __init__(self, parent, id):
        wx.Window.__init__(self, parent, id, pos=(40,0), size=(640,544))
        self.SetBackgroundColour(wx.Colour(76,134,174))
        self.shapes = []
        
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_PAINT, self.OnLevelPaint)

        self.placingActorId = -1
        self.placingActor = None
        self.startpt = None
        self.levelPosition = 0
        self.snap = True

        self.oldX = 0
        self.oldY = 0

    def OnMouseMove(self, evt):
        if self.placingActor is not None:
            if not self.snap:
                self.placingActor.pos = (evt.GetPosition()[0] - self.placingActor.bmp.GetWidth() / 2,
                    evt.GetPosition()[1] - self.placingActor.bmp.GetHeight() / 2)
            else:
                self.placingActor.pos = (int(evt.GetPosition()[0]/32)*32, int(evt.GetPosition()[1]/32)*32)
            self.Refresh()
        elif self.startpt is not None:
            if evt.GetPosition()[0] > self.startpt.pos[0]:
                distX = evt.GetPosition()[0] - self.startpt.pos[0]
            else:
                distX = evt.GetPosition()[0] - (self.startpt.pos[0] + self.startpt.bmp.GetWidth())
            if evt.GetPosition()[1] > self.startpt.pos[1]:
                distY = evt.GetPosition()[1] - self.startpt.pos[1]
            else:
                distY = evt.GetPosition()[1] - (self.startpt.pos[1] + self.startpt.bmp.GetHeight())
            nbX = int(distX/self.startpt.bmp.GetWidth())
            nbY = int(distY/self.startpt.bmp.GetHeight())
            if nbX >= 0:
                nbX = nbX + 1
            if nbY >= 0:
                nbY = nbY + 1

            if self.oldX == nbX and self.oldY == nbY:
                return

            for shape in self.placingBlock:
                self.shapes.remove(shape)
            self.placingBlock = []
            
            for x in range(0, nbX, distX/abs(distX)):
                for y in range(0, nbY, distY/abs(distY)):
                    s = Shape(self.startpt.id, (self.startpt.pos[0]+x*self.startpt.bmp.GetWidth(),
                        self.startpt.pos[1]+y*self.startpt.bmp.GetHeight()))
                    s.SetBitmap(self.startpt.image)
                    self.placingBlock.append(s)
                    self.shapes.append(s)
            self.Refresh()
            self.oldX = nbX
            self.oldY = nbY

    def OnLeftDown(self, evt):
        global file_modified
        debug("left down")
        if self.placingActor is None:
            self.placingActor = self.FindShape(evt.GetPosition())
            file_modified = True
        elif self.placingActor.type == 0:
            self.startpt = self.placingActor
            self.placingBlock = []

            self.placingActor = None
            self.placingActorId = -1

            file_modified = True

    def OnLeftUp(self, evt):
        debug("left up")
        if self.placingActor is not None:
            self.placingActor = None
            self.placingActorId = -1
        elif self.startpt is not None:
            self.placingBlock = []
            self.shapes.remove(self.startpt)
            self.startpt = None
            self.oldX = 0
            self.oldY = 0

    def OnRightDown(self, evt):
        global file_modified
        debug("right down")
        shape = self.FindShape(evt.GetPosition())
        if self.placingActor is None and self.startpt is None and shape:
            file_modified = True
            debug("context menu")
            self.selectedShape = shape
            if not hasattr(self, "popupID_PROPS"):
                self.popupID_PROPS = wx.NewId()
                self.popupID_DUP = wx.NewId()
                self.popupID_DEL = wx.NewId()
                self.Bind(wx.EVT_MENU, self.OnShapeProps, id=self.popupID_PROPS)
                self.Bind(wx.EVT_MENU, self.OnShapeDuplicate, id=self.popupID_DUP)
                self.Bind(wx.EVT_MENU, self.OnShapeRemove, id=self.popupID_DEL)
            menu = wx.Menu()
            menu.Append(self.popupID_PROPS, "Properties")
            menu.Append(self.popupID_DUP, "Duplicate")
            menu.Append(self.popupID_DEL, "Remove")
            self.PopupMenu(menu)
            menu.Destroy()

    def FindShape(self, pt):
        for shape in self.shapes:
            if shape.HitTest(pt):
                return shape
        return None

    def DrawShapes(self, dc):
        for shape in self.shapes:
            if shape.shown:
                shape.Draw(dc)

    def OnLevelPaint(self, evt):
        dc = wx.PaintDC(self)
        self.PrepareDC(dc)

        dc.SetPen(wx.Pen("Red"))
        dc.DrawLine(0,64,640,64)

        self.DrawShapes(dc)

    def OnShapeProps(self, evt):
        debug("shape props")
        dlg = ShapePropsDialog(self, -1, "Shape properties", self.selectedShape)
        dlg.ShowModal()

    def OnShapeDuplicate(self, evt):
        debug("shape duplicate")
        self.placingActor = Shape(self.selectedShape.id)
        self.placingActor.SetBitmap(self.selectedShape.image)
        self.shapes.append(self.placingActor)

    def OnShapeRemove(self, evt):
        debug("remove shape")
        self.shapes.remove(self.selectedShape)
        self.Refresh()

    def OnMoveLeft(self, evt):
        debug("Left Button cliked")
        if self.levelPosition <= 0:
            return
        for shape in self.shapes:
            oldpos = shape.pos
            shape.pos = (oldpos[0] + 32, oldpos[1])
            shape.shown = (shape.pos[0] + shape.bmp.GetWidth()) > 0 and shape.pos[0] < 640
        self.levelPosition = self.levelPosition - 32
        self.Refresh()
        if self.levelPosition == 0:
            self.GetGrandParent().btnL.Enable(False)

    def OnMoveRight(self, evt):
        debug("Right Button cliked")
        for shape in self.shapes:
            oldpos = shape.pos
            shape.pos = (oldpos[0] - 32, oldpos[1])
            shape.shown = (shape.pos[0] + shape.bmp.GetWidth()) > 0 and shape.pos[0] < 640
        self.levelPosition = self.levelPosition + 32
        self.Refresh()
        self.GetGrandParent().btnL.Enable(True)

class ToolsWindow(wx.MiniFrame):
    def __init__(self, parent, id):
        wx.MiniFrame.__init__(self, parent, id, "Tools", size=(120,200),style=wx.DEFAULT_FRAME_STYLE & ~ wx.RESIZE_BORDER)
        panel = wx.Panel(self)

        sizer = wx.GridSizer(0, 4, 2, 2)
        for actor in actorTypes.keys():
            BMP = wx.Image(imopj(actorTypes[actor][0]), wx.BITMAP_TYPE_GIF).Scale(16,16).ConvertToBitmap()
            btn = wx.BitmapButton(panel, -1, BMP, size=(26,26))
            actorsId[btn.GetId()] = actor
            sizer.Add(btn)
            self.Bind(wx.EVT_BUTTON, parent.OnToolClick, btn)
        panel.SetSizer(sizer)

class ShapePropsDialog(wx.Dialog):
    def __init__(self, parent, id, title, shape):
        wx.Dialog.__init__(self, parent, id, title, size=(245,125))
        sizer = wx.BoxSizer(wx.VERTICAL)

        hs = wx.BoxSizer(wx.HORIZONTAL)
        c = wx.TextCtrl(self, -1, shape.id)
        c.Enable(False)
        hs.Add(c, 0, wx.ALL, 5)

        if shape.type == 0:
            type = "Level"
        elif shape.type == 1:
            type = "Monster"
        else:
            type = "Other"
        c = wx.TextCtrl(self, -1, type)
        c.Enable(False)
        hs.Add(c, 0, wx.ALL, 5)
        sizer.Add(hs, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)

        hs = wx.BoxSizer(wx.HORIZONTAL)
        if shape.type == 0:
            c = wx.StaticText(self, -1, "Image:")
            hs.Add(c, 0, wx.ALL, 5)

            self.imageName = wx.TextCtrl(self, -1, shape.image, style=wx.TE_READONLY)
            hs.Add(self.imageName, 0, wx.ALL, 5)

            c = wx.Button(self, -1, "Browse")
            hs.Add(c, 0, wx.ALL, 5)
            self.Bind(wx.EVT_BUTTON, self.OnBrowse, c)
        elif shape.type == 1:
            c = wx.StaticText(self, -1, "Direction:")
            hs.Add(c, 0, wx.ALL, 5)

            c = wx.ComboBox(self, -1, str(shape.dir), style=wx.CB_READONLY, choices=["1","-1"])
            self.Bind(wx.EVT_COMBOBOX, self.OnDirectionChange, c)
            hs.Add(c, 0, wx.ALL, 5)
        sizer.Add(hs, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 0)
        #sizer.Add((0,0))
        c = wx.Button(self, wx.ID_OK)
        sizer.Add(c, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        #sizer.Layout()
        self.SetSizer(sizer)

    def OnBrowse(self, evt):
        resul = ChooseImageDialog(self, -1).ShowModal()
        if resul != wx.ID_CANCEL:
            self.imageName.SetValue(resul)
            self.GetParent().selectedShape.SetBitmap(resul)
            self.GetParent().Refresh()

    def OnDirectionChange(self, evt):
        newDir = int(evt.GetEventObject().GetValue())
        debug("change direction to %d" % newDir)
        if newDir != self.GetParent().selectedShape.dir:
            self.GetParent().selectedShape.SetDirectionalBitmap(newDir)
            self.GetParent().Refresh()

class ChooseImageDialog(wx.Dialog):
    def __init__(self, parent, id):
        from glob import glob
        wx.Dialog.__init__(self, parent, id, "Choose an image...", size=(260, 280))
        list = []
        imname = parent.imageName.GetValue()
        for file in glob("img"+os.sep+"*.gif"):
            list.append(file.split(os.sep)[1])
        self.list = wx.ListBox(self, -1, (5,5), (100,240), list, wx.LB_SINGLE)
        self.list.SetSelection(self.list.FindString(imname))
        self.ok = wx.Button(self, wx.ID_OK, pos=(170, 5))
        self.ok.Enable(False)
        wx.Button(self, wx.ID_CANCEL, pos=(170, 35))
        self.Bind(wx.EVT_LISTBOX, self.OnListClick, self.list)
        self.bmp = wx.StaticBitmap(self, -1, wx.Image(imopj(imname),
            wx.BITMAP_TYPE_GIF).ConvertToBitmap(), (110, 70))

    def OnListClick(self, evt):
        self.ok.Enable(True)
        self.bmp.Destroy()
        self.bmp = wx.StaticBitmap(self, -1, wx.Image(imopj(evt.GetString()),
            wx.BITMAP_TYPE_GIF).ConvertToBitmap(), (110,70))
        self.Refresh()

    def ShowModal(self):
        if wx.Dialog.ShowModal(self) != wx.ID_CANCEL:
            return self.list.GetString(self.list.GetSelection())
        return wx.ID_CANCEL

class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, "Pydza Editor v045")
        self.SetTopWindow(frame)

        frame.Show(True)
        return True
        
app = MyApp(False)
app.MainLoop()
