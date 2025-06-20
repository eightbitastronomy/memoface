import wx

class wxSubPanelQuick(wx.Panel):

    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__lookuphook = None
        if "lookup" in kwargs.keys():
            self.__lookuphook = kwargs["lookup"]
        self.__sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_lookup = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label="Quick lookup:",
                                    style=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.ST_ELLIPSIZE_END)
        entertxt_id = wx.NewId()
        self.__entertxt = wx.TextCtrl(self,
                                entertxt_id,
                                value="",
                                style=wx.TE_PROCESS_ENTER)
        label_lookup_x, label_lookup_y = label_lookup.GetTextExtent("Quick lookup")
        label_lookup.SetSize(wx.Size(label_lookup_x, label_lookup_y))
        entry_y = max(label_lookup_y, self.__entertxt.GetMinSize().y)
        entry_x = self.GetSize().x - label_lookup_x
        self.__sizer.Add(label_lookup, 0, wx.CENTRE, 0)
        self.__sizer.Add(self.__entertxt, 1, wx.EXPAND, 0)
        if self.__lookuphook is not None:
            self.__entertxt.Bind(wx.EVT_KEY_UP, lambda x: self.__lookuphook(x,self.__entertxt.GetValue()), self.__entertxt)
        self.SetSizer(self.__sizer)
        
        #self.add_standard_buttons("Cancel",
        #                        "Search",
        #                        (choice_panel, choice_sizer,))
        
        self.__entertxt.SetFocus()
    