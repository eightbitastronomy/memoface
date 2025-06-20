import wx


class wxFileFielder(wx.Panel):


    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        #self.parent = parent
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.__file_l = wx.StaticText(self,
                                    wx.ID_ANY,
                                    label="File:",
                                    style=wx.LEFT)
        file_txt_id = wx.NewId()
        self.__file_t = wx.TextCtrl(self,
                                file_txt_id,
                                value="",
                                style=wx.TE_PROCESS_ENTER)
        file_chooser_id = wx.NewId()
        self.__file_b = wx.Button(self,
                                  file_chooser_id,
                                  "Select")
        self.main_sizer.Add(self.__file_l, 0, wx.EXPAND, 0)
        self.main_sizer.Add(self.__file_t, 1, wx.EXPAND|wx.LEFT, 0)
        self.main_sizer.Add(self.__file_b, 0, wx.EXPAND, 0)
        self.SetSizer(self.main_sizer)
        active_dir = ""
        if "active" in kwargs.keys():
            active_dir = kwargs["active"]
        self.Bind(wx.EVT_BUTTON, lambda e: self.go_select(active_dir), self.__file_b, file_chooser_id)
        
    
    def go_select(self, active):
        with wx.FileDialog(self,
                           "Open file(s)",
                           defaultDir=active,
                           #wildcard=self._build_file_types(),#"Text (*.txt)|*.txt",
                           style=wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST) as openDialog:
            #if openDialog.ShowModal == wx.ID_CANCEL:
            #    return
            res = openDialog.ShowModal()
            if res == wx.ID_CANCEL:
                return
            file_names = openDialog.GetPaths()
            if file_names:
                self.__file_t.AppendText(" " + " ".join(file_names))
    
    
    def get_files(self):
        bufflist = []
        for i in range(0, self.__file_t.GetNumberOfLines()):
            bufflist += self.__file_t.GetLineText(i).split(" ")
        return list(filter(None, bufflist))