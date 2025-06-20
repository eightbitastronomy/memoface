import wx


class wxFileLoader(wx.Panel):


    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.mode = "load"
        if "mode" in kwargs.keys():
            self.mode = kwargs["mode"]
        self.loaded = ""
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.label = "File:"
        if "label" in kwargs.keys():
            self.label = kwargs["label"]
        file_chooser_id = wx.NewId()
        self.__file_b = wx.Button(self,
                                  file_chooser_id,
                                  "Select")
        self.__file_l = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label=self.label,
                                    style=wx.LEFT | wx.ELLIPSIZE_START)        
        self.main_sizer.Add(self.__file_b, 0, wx.EXPAND, 0)
        self.main_sizer.AddSpacer(5)
        self.main_sizer.Add(self.__file_l, 1, wx.ALIGN_CENTRE_VERTICAL, 0)
        self.SetSizer(self.main_sizer)
        active_dir = ""
        if "active" in kwargs.keys():
            active_dir = kwargs["active"]
        self.Bind(wx.EVT_BUTTON, lambda e: self.go_select(active_dir, self.__file_l), self.__file_b, file_chooser_id)
        
    
    def go_select(self, active, label):
        file_name = ""
        if self.mode == "save":
            with wx.FileDialog(self,
                            "Choose file for output",
                            defaultDir=active,
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as openDialog:
                res = openDialog.ShowModal()
                if res == wx.ID_CANCEL:
                    return
                file_name = openDialog.GetPath()
        else:
            with wx.FileDialog(self,
                            "Open file(s)",
                            defaultDir=active,
                            #wildcard=self._build_file_types(),#"Text (*.txt)|*.txt",
                            style=wx.FD_FILE_MUST_EXIST) as openDialog:
                #if openDialog.ShowModal == wx.ID_CANCEL:
                #    return
                res = openDialog.ShowModal()
                if res == wx.ID_CANCEL:
                    return
                file_name = openDialog.GetPath()
        if file_name:
            label.SetLabel("File: " + file_name)
            self.loaded = file_name
    
    
    def get_file(self):
        return self.loaded
