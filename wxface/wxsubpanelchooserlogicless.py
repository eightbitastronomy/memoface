import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem
from wxface.wxsubpanelquick import wxSubPanelQuick


class wxSubPanelChooserLogicless(wx.Panel):
    
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__selection = []
        self.__table = []
        if "table" in kwargs.keys():
            self.__table = [ MarkViewItem(item, lambda x: x) for item in kwargs["table"] ]
        self.__default = ""
        if "default" in kwargs.keys():
            self.__default = kwargs["default"]
        self.__listbox = wxMarkView(self, self.__table)
        self.__listbox.SetListView(self.__selection)
        self.__sizer.Add(self.__listbox, 1, wx.EXPAND, 0)
        kwargs["lookup"] = self.on_quick_scroll
        self.__quickpanel = wxSubPanelQuick(self, **kwargs) #need to pass in a text label, but need this from subpanelchooser
        #self.__quickpanel.SetSize(wx.Size(self.__quickpanel.GetBestSize().GetWidth()-150, self.__quickpanel.GetBestSize().GetHeight()))
        self.__sizer.Add(self.__quickpanel, 0, wx.EXPAND, 0)
        self.__sizer.AddSpacer(5)
        self.SetSizer(self.__sizer)
        

    def on_quick_scroll(self, event, word):
        if word == "":
            self.__listbox.EnsureVisible(0)
        else:
            for i, item in enumerate(self.__table):
                if item.txt().find(word, 0, len(word)) > -1:
                    self.__listbox.EnsureVisible(i)
        event.Skip()
        
    
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
            
    def clear_selection(self):
        for i in range(0, self.__listbox.GetItemCount()):
            self.__listbox.Select(i,0)