import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem
from wxface.wxsubpanelquick import wxSubPanelQuick
from wxface.wxsubpanelradio import wxSubPanelRadio


class wxSubPanelChooser(wx.Panel):
    
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__selection = []
        self.__logic = "OR"
        self.__table = []
        if "table" in kwargs.keys():
            self.__table = [ MarkViewItem(item, lambda x: x) for item in kwargs["table"] ]
        self.__default = ""
        if "default" in kwargs.keys():
            self.__default = kwargs["default"]
        self.__listbox = wxMarkView(self, self.__table)
        self.__listbox.SetListView(self.__selection)
        self.__sizer.Add(self.__listbox, 1, wx.EXPAND, 0)
        #make a class for the quickpanel using what's in memoface
        kwargs["lookup"] = self.on_quick_scroll
        self.__quickpanel = wxSubPanelQuick(self, **kwargs) #need to pass in a text label, but need this from subpanelchooser
        self.__sizer.Add(self.__quickpanel, 0, wx.EXPAND, 0)
        self.__sizer.AddSpacer(5)
        if "target" in kwargs.keys():
            self.__radiopanel = wxSubPanelRadio(self, label=kwargs["target"], hook=self.clear_selection)
        else:
            self.__radiopanel = wxSubPanelRadio(self, hook=self.clear_selection)
        self.__sizer.Add(self.__radiopanel, 0, wx.EXPAND, 0)
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
        
        
    def get_logic(self):
        return self.__radiopanel.get_value()
       
    
    def get_all(self):
        #bufferlist = []
        #for i in range(0, self.__listbox.GetItemCount()):
        #    bufferlist.extend(self.__listbox.GetItem(i).GetText())
        #return bufferlist
        return [self.__listbox.GetItem(i).GetText() for i in range(0, self.__listbox.GetItemCount())]
    
    def get_selection(self):
        self.__selection.clear()
        itemnum = self.__listbox.GetFirstSelected()
        while itemnum > -1:
            buf = self.__listbox.GetItem(itemnum).GetText()
            self.__selection.append(buf)
            itemnum = self.__listbox.GetNextSelected(itemnum)
        return self.__selection
        
    
    def set_selection(self, n):
        if n < 0:
            for i in range(0, self.__listbox.GetItemCount()):
                self.__listbox.Select(i,0)
        else:
            self.__listbox.Select(n, 1)
            
            
    def clear_selection(self):
        for i in range(0, self.__listbox.GetItemCount()):
            self.__listbox.Select(i,0)


    def refresh(self, datalist):
        self.__listbox.clear()
        self.__listbox.set_data([MarkViewItem(item, lambda x: x) for item in datalist])
        #self.__listbox.Refresh()
