import wx


class wxSubPanelRadio(wx.Panel):
    
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        logic_labeler = ""
        if "label" in kwargs.keys():
            logic_labeler = kwargs["label"]
        self.__sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_logic = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label="Filter using... ",
                                    style=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.ST_ELLIPSIZE_END)
        self.__sizer.Add(label_logic, 0, wx.CENTRE, 0) #wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.__radio_or = wx.RadioButton(self,
                                        wx.ID_ANY,
                                        " any ",
                                        style = wx.RB_GROUP )
        self.__radio_and = wx.RadioButton(self,
                                        wx.ID_ANY,
                                        " all ")
        self.__sizer.Add(self.__radio_or, 0, wx.ALIGN_CENTRE, 5)# |wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.__sizer.Add(self.__radio_and, 0, wx.ALIGN_CENTRE, 5)#|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        if logic_labeler:
            label_end = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label="... " + logic_labeler,
                                    style=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.ST_ELLIPSIZE_END)
            self.__sizer.Add(label_end, 0, wx.CENTRE, 0)
        self.__sizer.AddStretchSpacer()
        clear_btn_id = wx.NewId()
        self.__clear = wx.Button(self,
                                clear_btn_id,
                                "Clear selection")
        self.__sizer.Add(self.__clear, 0, wx.ALIGN_CENTRE_VERTICAL, 0)
        self.SetSizer(self.__sizer)
        if "hook" in kwargs.keys():
            self.__hook = kwargs["hook"]
            self.Bind(wx.EVT_BUTTON, lambda e: self.__hook(), self.__clear, clear_btn_id)

        
    def get_value(self):
        if self.__radio_or.GetValue():
            return "OR"
        else:
            return "AND"