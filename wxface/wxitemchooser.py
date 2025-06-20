import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem
from wxface.wxsubpanelquick import wxSubPanelQuick


class wxItemChooser(wx.Panel):
    
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__sizer = wx.GridBagSizer()
        self.__selection = []
        self.__table = []
        if "table" in kwargs.keys():
            self.__table = [ MarkViewItem(item, lambda x: x) for item in kwargs["table"] ]
        find_text = "Find items"
        if "labelleft" in kwargs.keys():
            find_text = kwargs["labelleft"]
        rem_text = "Remove selected"
        if "labelright" in kwargs.keys():
            find_text = kwargs["labelright"]
        self.__default = ""
        if "default" in kwargs.keys():
            self.__default = kwargs["default"]
        banner_label = "Items:"
        if "label" in kwargs.keys():
            banner_label = kwargs["label"]
        self.__banner = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label=banner_label,
                                    style=wx.LEFT | wx.ELLIPSIZE_START)
        self.__listbox = wxMarkView(self, self.__table)
        self.__listbox.SetListView(self.__selection)
        find_id = wx.NewId()
        self.__find = wx.Button(self, 
                                find_id,
                                find_text)
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.find_items(),
                self.__find)
        rem_id = wx.NewId()
        self.__remove = wx.Button(self,
                                rem_id,
                                rem_text)
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.remove_selection(),
                self.__remove)
        self.__sizer.Add(self.__banner, (0,0), (1,2), flag=wx.EXPAND)
        self.__sizer.Add(self.__listbox, (1,0), (2,2), flag=wx.EXPAND)
        self.__sizer.Add(self.__find, (3,0), (1,1), flag=wx.EXPAND)
        self.__sizer.Add(self.__remove, (3,1), (1,1), flag=wx.EXPAND)
        self.SetSizer(self.__sizer)


    def find_items(self):
        paths = []
        with wx.DirDialog(self, 
                    "Choose directories", 
                    "", 
                    #wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.DD_MULTIPLE) as dirmessage:
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as dirmessage:
            res = dirmessage.ShowModal()
            if res == wx.ID_OK:
                path = dirmessage.GetPath()
                #dirmessage.GetPaths(paths)
        self.insert([path])
        
    
    def insert(self, items):
        for item in items:
            if not item in [x.txt() for x in self.__table]:
                self.__table.append(MarkViewItem(item, lambda x: x))
                self.__listbox.SetItemCount(len(self.__table))
    

    def remove_selection(self):
        ##for i in range(0, self.__listbox.GetItemCount()):
        ##    pass
        #indices = []
        #itemnum = self.__listbox.GetFirstSelected()
        #while itemnum > -1:
        #    indices.append(itemnum)
        #    itemnum = self.__listbox.GetNextSelected(itemnum)
        #for index in sorted(indices, reverse=True):
        #    self.__table.pop(index)
        #self.__listbox.SetItemCount(len(self.__table))
        #self.__listbox.RefreshItems(0,len(self.__table)-1)
        self.__listbox.remove_selected()
        
    
    def get_selection(self):
        self.__selection.clear()
        itemnum = self.__listbox.GetFirstSelected()
        while itemnum > -1:
            buf = self.__listbox.GetItem(itemnum).GetText()
            self.__selection.append(buf)
            itemnum = self.__listbox.GetNextSelected(itemnum)
        return self.__selection
        
        
    def get_selection_mvi(self):
        selection = []
        itemnum = self.__listbox.GetFirstSelected()
        while itemnum > -1:
            selection.append(MarkViewItem(self.__listbox.GetItem(itemnum).GetText(), lambda x: x))
            itemnum = self.__listbox.GetNextSelected(itemnum)
        return selection
        
    
    def set_selection(self, n):
        if n < 0:
            for i in range(0, self.__listbox.GetItemCount()):
                self.__listbox.Select(i,0)
        else:
            self.__listbox.Select(n, 1)


    def get_all(self):
        #bufferlist = []
        #for i in range(0, self.__listbox.GetItemCount()):
        #    bufferlist.extend(self.__listbox.GetItem(i).GetText())
        #return bufferlist
        return [self.__listbox.GetItem(i).GetText() for i in range(0, self.__listbox.GetItemCount())]
    
    
    def clear_selection(self):
        for i in range(0, self.__listbox.GetItemCount()):
            self.__listbox.Select(i,0)
