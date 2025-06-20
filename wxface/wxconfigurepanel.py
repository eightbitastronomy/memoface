import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem


class wxConfigurePanel(wx.Panel):


    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__descr_txt = "Configuration:"
        if "descr" in kwargs.keys():
            self.__descr_txt = kwargs["descr"]
        self.__descr = wx.StaticText(
                                self,
                                wx.ID_ANY,
                                label=self.__descr_txt,
                                style=wx.LEFT)
        self.__txt_fields = {}
        if "text" in kwargs.keys():
            for (k,v,d) in kwargs["text"]:
                self.__txt_fields[k] = (
                    wx.StaticText(
                        self,
                        wx.ID_ANY,
                        label=v,
                        style=wx.LEFT | wx.ELLIPSIZE_START),
                    wx.TextCtrl(
                        self,
                        wx.ID_ANY,
                        value=d,
                        style=wx.TE_PROCESS_ENTER)
                )
        self.__dir_fields = {}
        if "dir" in kwargs.keys():
            for (k1,v1,d1) in kwargs["dir"]:
                self.__dir_fields[k1] = (
                    wx.StaticText(
                        self,
                        wx.ID_ANY,
                        label=v1,
                        style=wx.LEFT | wx.ELLIPSIZE_START),
                    wx.TextCtrl(
                        self,
                        wx.ID_ANY,
                        value=d1,
                        style=wx.TE_PROCESS_ENTER),
                    wx.Button(self,
                        wx.ID_ANY,
                        "Select")
                )
                self.Bind(
                    wx.EVT_BUTTON,
                    lambda e: self.__call_dialog(e, self.__dir_fields[k1][1], self.__dir_fields[k1][0]),
                    self.__dir_fields[k1][2])
        self.__check_boxes = {}
        if "check" in kwargs.keys():
            for (k2,v2) in kwargs["check"]:
                self.__check_boxes[k2] = wx.CheckBox(
                        self,
                        label=v2,
                        id=wx.ID_ANY)
                self.__check_boxes[k2].SetValue(False)
        self.__check_lists = {}
        if "list" in kwargs.keys():
            for (k3,v3,t3,d3) in kwargs["list"]:
                self.__check_lists[k3] = (
                    wx.CheckBox(
                        self, 
                        label=v3,
                        id=wx.ID_ANY),
                    wx.StaticText(
                        self,
                        wx.ID_ANY,
                        label=t3,
                        style=wx.LEFT),
                    wxMarkView(
                        self,
                        [MarkViewItem(item, lambda x: x) for item in d3],
                        single=True)
                )
                self.__check_lists[k3][0].SetValue(False)
        self.__sizer = wx.GridBagSizer()
        #numrows = len(self.__txt_fields) + len(self.__dir_fields) + len(self.__check_boxes) + 3*len(self.__check_lists)
        #numcols = 3
        self.__sizer.Add(self.__descr, (0,0), (1,2), flag=wx.EXPAND)
        i = 1
        self.__sizer.Add(wx.Size(5,5), (i,0))
        #self.__sizer.AddGrowableRow(1)
        i += 1
        for k4 in self.__txt_fields.keys():
            self.__sizer.Add(self.__txt_fields[k4][0], (i,0), (1,1), flag=wx.EXPAND)
            self.__sizer.Add(self.__txt_fields[k4][1], (i,1), (1,1), flag=wx.EXPAND)
            i += 1
        for k5 in self.__dir_fields.keys():
            self.__sizer.Add(self.__dir_fields[k5][0], (i,0), (1,1), flag=wx.EXPAND)
            self.__sizer.Add(self.__dir_fields[k5][2], (i,1), (1,1), flag=wx.EXPAND)
            self.__sizer.Add(self.__dir_fields[k5][1], (i,2), (1,1), flag=wx.EXPAND)
            i += 1
        for k6 in self.__check_boxes.keys():
            self.__sizer.Add(self.__check_boxes[k6], (i,0), (1,1), flag=wx.EXPAND)
            i += 1
        for k7 in self.__check_lists.keys():
            self.__sizer.Add(self.__check_lists[k7][0], (i,0), (1,1), flag=wx.EXPAND)
            self.__sizer.Add(self.__check_lists[k7][1], (i,1), (1,1), flag=wx.EXPAND)
            self.__sizer.Add(self.__check_lists[k7][2], (i,2), (3,1), flag=wx.EXPAND)
            i += 3
        #self.__sizer.AddGrowableCol(0)
        if self.__check_lists.keys() or self.__dir_fields.keys():
            self.__sizer.AddGrowableCol(2)
        self.SetSizer(self.__sizer)
        
        
    def get_txt_value(self, key):
        result = ""
        if key in self.__txt_fields.keys():
            result = self.__txt_fields[key][1].GetLineText(0)
        return result
            
    
    def get_dir_value(self, key):
        result = ""
        if key in self.__dir_fields.keys():
            result = self.__dir_fields[key][1].GetLineText(0)
        return result
            
            
    def get_check_box(self, key):
        result = False
        if key in self.__check_boxes.keys():
            result = self.__check_boxes[key].GetValue()
        return result
            
    
    def get_check_list(self, key):
        result = ""
        if key in self.__check_lists.keys():
            if self.__check_lists[key][0].GetValue() == True:
                selection = self.__check_lists[key][2].GetFirstSelected()
                if selection > -1:
                    result = self.__check_lists[key][2].GetItem(selection).GetText()
                if result == "":
                    result = "%INVALIDSELECTION%"
        return result

                
    def __call_dialog(self, event, field, text):
        with wx.DirDialog(
                self,
                "Choose directory",
                "",
                wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as chooser:
            res = chooser.ShowModal()
            if res == wx.ID_OK:
                field.write(chooser.GetPath())