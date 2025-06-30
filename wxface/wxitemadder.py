import wx
from wxface.wxsubpanelchooserlogicless import wxSubPanelChooserLogicless
from wxface.wxmarkview import wxMarkView, MarkViewItem


class wxItemAdder(wx.Panel):

    def __init__(self, parent, toc, **kwargs):
        wx.Panel.__init__(self, parent)
        self.size = self.GetSize()
        if "width" in kwargs.keys():
            self.size = kwargs["width"]
        self.main_sizer = wx.GridBagSizer()
        itemslabel = "Item:"
        itemsrightlabel = "Existing items:"
        if "label" in kwargs.keys():
            itemslabel = kwargs["label"]
        if "labelright" in kwargs.keys():
            itemsrightlabel = kwargs["labelright"]
        self.tocright = []
        if "tocright" in kwargs.keys():
            self.tocright = kwargs["tocright"]
        self.__additions = []
        self.__removals = []
        mode = "add"
        if "mode" in kwargs.keys():
            mode = kwargs["mode"]
        if mode == "add":
            self.__item_l = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label=itemslabel,
                                    style=wx.LEFT)
            item_txt_id = wx.NewId()
            self.__item_t = wx.TextCtrl(self,
                                    item_txt_id,
                                    value="",
                                    style=wx.TE_PROCESS_ENTER)
            manual_adder_id = wx.NewId()
            self.__manualadder_b = wx.Button(self,
                                            manual_adder_id,
                                            "Add >")
            self.Bind(wx.EVT_BUTTON, lambda e: self.add_from_manual(), self.__manualadder_b, manual_adder_id)
            self.__listadder = wxSubPanelChooserLogicless(self, table=toc)
            self.__listadder.SetSize(wx.Size(int(self.size.GetWidth()/3), self.GetBestSize().GetHeight()))
            list_adder_id = wx.NewId()
            self.__listadder_b = wx.Button(self,
                                            list_adder_id,
                                            "Add >")
            self.Bind(wx.EVT_BUTTON, lambda e: self.add_from_box(), self.__listadder_b, list_adder_id)
            self.__targetlist = wxMarkView(self, self.tocright)
            target_remove_id = wx.NewId()
            self.__targetrem_b = wx.Button(self,
                                            target_remove_id,
                                            "Remove Selected")
            self.Bind(wx.EVT_BUTTON, lambda e: self.rem_from_box(), self.__targetrem_b, target_remove_id)
            self.main_sizer.Add(self.__item_l, (0,0), (3,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__item_t, (0,1), (1,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__manualadder_b, (0,2), (1,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__listadder, (1,1), (4,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__listadder_b, (1,2), (2,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__targetlist, (0,3), (4,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__targetrem_b, (4,3), (1,1))#, flag=wx.EXPAND)
            self.main_sizer.AddGrowableCol(0)
            self.main_sizer.AddGrowableCol(1)
            self.main_sizer.AddGrowableCol(2)
            self.main_sizer.AddGrowableCol(3)
        else:
            self.__item_l = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label=itemslabel,
                                    style=wx.LEFT)
            self.__itemright_l = wx.StaticText(self,
                                            wx.ID_ANY,
                                            label=itemsrightlabel,
                                            style=wx.LEFT)
            item_txt_id = wx.NewId()
            self.__item_t = wx.TextCtrl(self,
                                    item_txt_id,
                                    value="",
                                    style=wx.TE_PROCESS_ENTER)
            manual_adder_id = wx.NewId()
            self.__manualadder_b = wx.Button(self,
                                            manual_adder_id,
                                            "Add >")
            self.Bind(wx.EVT_BUTTON, lambda e: self.add_from_manual(), self.__manualadder_b, manual_adder_id)
            self.__listadder = wxSubPanelChooserLogicless(self, table=toc)
            self.__listadder.SetSize(wx.Size(int(self.size.GetWidth()/3), self.GetBestSize().GetHeight()))
            list_adder_id = wx.NewId()
            self.__listadder_b = wx.Button(self,
                                            list_adder_id,
                                            "Add >")
            self.Bind(wx.EVT_BUTTON, lambda e: self.add_from_box(), self.__listadder_b, list_adder_id)
            self.__targetlist = wxMarkView(self, [ MarkViewItem(item, lambda x: x) for item in self.tocright ])
            target_remove_id = wx.NewId()
            self.__targetrem_b = wx.Button(self,
                                            target_remove_id,
                                            "Remove Selected")
            self.Bind(wx.EVT_BUTTON, lambda e: self.rem_from_box(), self.__targetrem_b, target_remove_id)
            self.main_sizer.Add(self.__item_l, (0,0), (1,2), flag=wx.EXPAND)
            self.main_sizer.Add(self.__itemright_l, (0,2), (1,2), flag=wx.EXPAND)
            self.main_sizer.Add(self.__item_t, (1,0), (1,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__manualadder_b, (1,1), (1,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__listadder, (2,0), (4,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__listadder_b, (2,1), (2,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__targetlist, (1,2), (3,1), flag=wx.EXPAND)
            self.main_sizer.Add(self.__targetrem_b, (4,2), (1,1))#, flag=wx.EXPAND)
            self.main_sizer.AddGrowableCol(0)
            self.main_sizer.AddGrowableCol(1)
            self.main_sizer.AddGrowableCol(2)
            #self.main_sizer.AddGrowableCol(3)
        self.SetSizer(self.main_sizer)
    
    def add_from_box(self):
        buffer = self.__listadder.get_selection_mvi()
        for item in buffer:
            self.__targetlist.Insert(item)
            self.__additions.append(item.txt())
        #self.__targetlist.SetListView(self.__listadder.get_selection_raw())
        self.__listadder.clear_selection()
        
        
    def rem_from_box(self):
        self.__removals = [] #.extend(self.__targetlist.get_selection())
        #self.__selection.clear()
        itemnum = self.__targetlist.GetFirstSelected()
        while itemnum > -1:
            buf = self.__targetlist.GetItem(itemnum).GetText()
            self.__removals.append(buf)
            itemnum = self.__targetlist.GetNextSelected(itemnum)
        self.__targetlist.remove_selected()
        
    
    def add_from_manual(self):
        items = []
        numtextlines = self.__item_t.GetNumberOfLines()
        for i in range(0, numtextlines):
            items += [ MarkViewItem(x, lambda y: y) for x in self.__item_t.GetLineText(i).split(" ") ]
        for item in items:
            self.__targetlist.Insert(item)
            self.__additions.append(item.txt())
        
        
    #def get(self):
    #    retlist = []
    #    for i in range(0, self.__targetlist.GetItemCount()):
    #        retlist.append(self.__targetlist.GetItem(i).GetText())
    #    return retlist


    # Doesn't appear that the self.tocright needs to be returned
    def get(self):
        if self.__additions and self.__removals:
            for item in self.__removals:
                if item in self.__additions:
                    self.__removals.remove(item)
                    self.__additions.remove(item)
        return (self.tocright, self.__additions, self.__removals)


    def set(self, items):
        self.tocright = items
        self.__targetlist.set_data([MarkViewItem(x, lambda y: y) for x in items])
