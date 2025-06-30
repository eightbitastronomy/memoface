import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem


class wxItemFilterer(wx.Panel):


    def __init__(self, parent, table, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__selection = []
        self.__table = []
        self.main_sizer = wx.GridBagSizer()
        ##self.main_sizer = wx.BoxSizer()
        self.__cb = wx.CheckBox(self, wx.ID_ANY)
        self.__cb.SetValue(False)
        ##if "table" in kwargs.keys():
        if table:
            self.__table = [ MarkViewItem(item, lambda x: x) for item in table ]
        self.__default = "By Option:"
        if "default" in kwargs.keys():
            self.__default = kwargs["default"]
        self.__lab = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label=self.__default,
                                    style=wx.LEFT)
        self.__list = wxMarkView(self, self.__table)
        self.__list.SetListView(self.__selection)
        self.main_sizer.Add(self.__cb, (0,0), (1,1), flag=wx.EXPAND)
        ##self.main_sizer.Add(self.__cb, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        ##self.main_sizer.AddSpacer(5)
        self.main_sizer.Add(self.__lab, (0,1), (1,1), flag=wx.EXPAND)
        ##self.main_sizer.Add(self.__lab, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.main_sizer.Add(self.__list, (0,2), (2,1), flag=wx.EXPAND)
        ##self.main_sizer.Add(self.__list, 0, wx.EXPAND, 0)
        ##self.main_sizer.AddGrowableCol(0)
        ##self.main_sizer.AddGrowableCol(1)
        self.main_sizer.AddGrowableCol(2)
        self.SetSizer(self.main_sizer)
    
    
    #def is_checked(self):
    #    return self.__cb.GetValue()


    def get_selection(self):
        self.__selection.clear()
        itemnum = self.__list.GetFirstSelected()
        while itemnum > -1:
            buf = self.__list.GetItem(itemnum).GetText()
            self.__selection.append(buf)
            itemnum = self.__list.GetNextSelected(itemnum)
        return self.__selection
