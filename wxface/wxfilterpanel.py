import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem


class wxFilterPanel(wx.Panel):

    
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent)
        self.__rem_first = wx.StaticText(self,
                                        wx.ID_ANY,
                                        label = "Include?",
                                        style = wx.LEFT)
        self.__mainsizer = wx.GridBagSizer()
        self.__rb_opt_file = wx.RadioButton(self, id=wx.ID_ANY, style=wx.RB_GROUP)
        self.__rb_opt_mark = wx.RadioButton(self, id=wx.ID_ANY)
        self.__rb_opt_type = wx.RadioButton(self, id=wx.ID_ANY)
        self.__rb_opt_file.SetValue(True)
        if "filelabel" in kwargs.keys():
            self.__file_label = kwargs["filelabel"]
        else:
            self.__file_label = "By Option:"
        self.__lab_file = wx.StaticText(self,
                                        wx.ID_ANY,
                                        label=self.__file_label,
                                        style=wx.LEFT)
        file_txt_id = wx.NewId()
        self.__tc_file = wx.TextCtrl(self,
                                file_txt_id,
                                value="",
                                style=wx.TE_PROCESS_ENTER)
        file_chooser_id = wx.NewId()
        self.__b_file = wx.Button(self,
                                  file_chooser_id,
                                  "Select")
        active_dir = ""
        if "active" in kwargs.keys():
            active_dir = kwargs["active"]
        self.Bind(wx.EVT_BUTTON, lambda e: self.go_select(active_dir), self.__b_file, file_chooser_id)
        if "marktable" in kwargs.keys():
            self.__mark_table = [ MarkViewItem(item, lambda x: x) for item in kwargs["marktable"] ]
        else:
            self.__mark_table = []
        self.__mark_label = "By Option:"
        if "marklabel" in kwargs.keys():
            self.__mark_label = kwargs["marklabel"]
        self.__lab_mark = wx.StaticText(self,
                                        wx.ID_ANY,
                                        label=self.__mark_label,
                                        style=wx.LEFT)
        self.__mv_mark = wxMarkView(self, self.__mark_table, single=True)
        self.__selection_mark = []
        self.__mv_mark.SetListView(self.__selection_mark)
        if "typetable" in kwargs.keys():
            self.__type_table = [ MarkViewItem(item, lambda x: x) for item in kwargs["typetable"] ]
        else:
            self.__type_table = []
        self.__type_label = "By Option:"
        if "typelabel" in kwargs.keys():
            self.__type_label = kwargs["typelabel"]
        self.__lab_type = wx.StaticText(self,
                                        wx.ID_ANY,
                                        label=self.__type_label,
                                        style=wx.LEFT)
        self.__mv_type = wxMarkView(self, self.__type_table, single=True)
        self.__selection_type = []
        self.__mv_type.SetListView(self.__selection_type)
        self.__rem_warn = wx.StaticText(self,
                                        wx.ID_ANY,
                                        label = "Removals must match all selected criteria.",
                                        style = wx.LEFT)
        self.__mainsizer.Add(self.__rem_first, (0,0), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__rb_opt_file, (1,0), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__rb_opt_mark, (3,0), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__rb_opt_type, (5,0), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__lab_file, (1,1), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__lab_mark, (3,1), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__lab_type, (5,1), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__b_file, (1,2), (1,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__tc_file, (1,3), (2,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__mv_mark, (3,3), (2,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__mv_type, (5,3), (2,1), flag=wx.EXPAND)
        self.__mainsizer.Add(self.__rem_warn, (7,0), (1,3), flag=wx.EXPAND)
        self.__mainsizer.AddGrowableCol(1)
        self.__mainsizer.AddGrowableCol(3)
        self.SetSizer(self.__mainsizer)

    def go_select(self, active):
        with wx.FileDialog(self,
                           "Open file(s)",
                           defaultDir=active,
                           style=wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST) as openDialog:
            res = openDialog.ShowModal()
            if res == wx.ID_CANCEL:
                return
            file_names = openDialog.GetPaths()
            if file_names:
                self.__tc_file.AppendText(" " + " ".join(file_names))
                self.__rb_opt_file.SetValue(True)
    

    def get_values(self):
        if self.__rb_opt_file.GetValue():
            return ("file", self.__get_files())
        if self.__rb_opt_mark.GetValue():
            return ("mark", self.__get_marks())
        if self.__rb_opt_type.GetValue():
            return ("type", self.__get_types())

    
    def __get_files(self):
        bufflist = []
        for i in range(0, self.__tc_file.GetNumberOfLines()):
            bufflist += self.__tc_file.GetLineText(i).split(" ")
        return list(filter(None, bufflist))


    def __get_marks(self):
        self.__selection_mark.clear()
        itemnum = self.__mv_mark.GetFirstSelected()
        while itemnum > -1:
            buf = self.__mv_mark.GetItem(itemnum).GetText()
            self.__selection_mark.append(buf)
            itemnum = self.__mv_mark.GetNextSelected(itemnum)
        return self.__selection_mark


    def __get_types(self):
        self.__selection_type.clear()
        itemnum = self.__mv_type.GetFirstSelected()
        while itemnum > -1:
            buf = self.__mv_type.GetItem(itemnum).GetText()
            self.__selection_type.append(buf)
            itemnum = self.__mv_type.GetNextSelected(itemnum)
        return self.__selection_type

