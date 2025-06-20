import wx


class wxSubPanelCheck(wx.Panel):


    def __init__(self, parent, optiontuple, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__options = {}
        #self.__sizer = wx.BoxSizer(wx.VERTICAL)
        self.__sizer = wx.BoxSizer(wx.HORIZONTAL)
        #if "title" in kwargs.keys():
        #    titler = wx.StaticText(self,
        #                            wx.ID_ANY,
        #                            label=kwargs["title"],
        #                            style=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.ST_ELLIPSIZE_END)
        #    self.__sizer.Add(titler, 0, wx.CENTRE, 0) #wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        for t in optiontuple:
            #labeler = wx.StaticText(self,
            #                        wx.ID_ANY,
            #                        label=t,
            #                        style=wx.ALIGN_LEFT | wx.ST_ELLIPSIZE_END)
            box = wx.CheckBox(self,
                            wx.ID_ANY,
                            label=t,
                            #style=wx.ALIGN_LEFT)
                            style=wx.ALIGN_CENTRE)
            box.SetValue(False)
            #self.__sizer.Add(labeler, 0, wx.CENTRE, 0)
            self.__sizer.Add(box, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 0)
            self.__options[t] = box
        self.SetSizer(self.__sizer)
        

    def get_value(self, label):
        if label in self.__options.keys():
            if self.__options[label].IsChecked():
                return "true"
            else:
                return "false"
        return "false"