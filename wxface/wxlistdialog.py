import wx
from wxface.wxmarkview import wxMarkView



class wxListDialog(wx.Dialog):

    def __init__(self, parent, table, **kwargs):
        self.table = table
        if "title" in kwargs.keys():
            dtitle = kwargs["title"]
        else:
            dtitle = "Select..."
        if "ret" in kwargs.keys():
            self.ret = kwargs["ret"]
        else:
            self.ret = None
        if "conf" in kwargs.keys():
            self.conf_hook = kwargs["conf"]
        else:
            self.conf_hook = None
        if "edit" in kwargs.keys():
            self.editable = kwargs["edit"]
        else:
            self.editable = False
        wx.Dialog.__init__(self,
                           parent,
                           wx.ID_ANY,
                           title=dtitle,
                           style=wx.RESIZE_BORDER | wx.CAPTION | wx.CLOSE_BOX)
        self.selection = [] 
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.listbox = wxMarkView(self, self.table)
        self.listbox.SetListView(self.selection)
        self.main_sizer.Add(self.listbox, 1, wx.EXPAND, 0)
        self.SetSizer(self.main_sizer)
        self.choice_panel = None
        self.choice_sizer = None
        
    def add_standard_buttons(self, canceltitle="Cancel", okaytitle="OK", contpair=None):
        if contpair:
            if not len(contpair) == 2:
                return
            self.choice_panel = contpair[0]
            self.choice_sizer = contpair[1]
        else:
            self.choice_panel = wx.Panel(self)
            self.main_sizer.Add(self.choice_panel)
            self.choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        choice_cancel_id = wx.NewId()
        choice_cancel = wx.Button(self.choice_panel,
                                  choice_cancel_id,
                                  canceltitle)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, choice_cancel)
        choice_cancel.SetSize(choice_cancel.GetBestSize())
        choice_okay_id = wx.NewId()
        choice_okay = wx.Button(self.choice_panel,
                                choice_okay_id,
                                okaytitle)
        choice_okay.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.on_okay, choice_okay)
        choice_okay.SetSize(choice_okay.GetBestSize())
        self.choice_sizer.Add(choice_cancel, 1, wx.EXPAND, 0)
        self.choice_sizer.Add(choice_okay, 1, wx.EXPAND, 0)
        self.choice_panel.SetSizer(self.choice_sizer)

    def on_okay(self, event):
        #dprint(3, "\nwxListDialog::on_okay")
        pass

    def on_cancel(self, event):
        #dprint(3, "\nwxListDialog::on_cancel")
        #self.SetReturnCode(-1)
        self.EndModal(-1)
        self.Destroy()

    def set_conf(self, hook):
        self.conf_hook = hook

    def set_table(self, table):
        self.table = table

    def set_return(self, r):
        self.ret = r
