import wx
from wxface.wxmarkdialogselect import wxMarkDialogSelect
from wxface.wxmarkview import MarkViewItem


class wxPMPanel(wx.Panel):

    def __init__(self, parent, table, **kwargs):
        self.table = table
        if "title" in kwargs.keys():
            dtitle = kwargs["title"]
        else:
            dtitle = "Select..."
        self.conf_hook = None
        if "conf" in kwargs.keys():
            self.conf_hook = kwargs["conf"]
        wx.Panel.__init__(self, parent)
        self.selection = [] 
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.listbox = None
        self.choice_panel = None
        self.choice_sizer = None
        if "view" in kwargs.keys():
            self.add_list_box(kwargs["view"])
            #cpanel, csizer = self.add_pmf()
            self.choice_panel, self.choice_sizer = self.add_pmf()
            #self.add_standard_buttons("Cancel", "Apply", (cpanel,csizer,))
        self.SetSizer(self.main_sizer)

    def add_list_box(self, lb, parent=None, table=None):
        if not parent:
            parent = self
        if not table:
            table = []
        self.listbox = lb(parent, table)
        self.main_sizer.Add(self.listbox, 1, wx.EXPAND, 0)

    def add_pmf(self, parent=None):
        if not parent:
            parent = self
        control_panel = wx.Panel(parent)
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ctrl_minus = wx.Button(control_panel,
                               wx.ID_ANY,
                               "  -  ")
        ctrl_minus.Bind(wx.EVT_BUTTON, self.on_minus_button, ctrl_minus)
        ctrl_plus = wx.Button(control_panel,
                               wx.ID_ANY,
                               "  +  ")
        ctrl_plus.Bind(wx.EVT_BUTTON, self.on_plus_button, ctrl_plus)
        ctrl_find = wx.Button(control_panel,
                                wx.ID_ANY,
                                " Find ")
        ctrl_find.Bind(wx.EVT_BUTTON, self.on_find, ctrl_find)
        control_sizer.Add(ctrl_minus, 1, wx.LEFT|wx.RIGHT, 0)
        control_sizer.Add(ctrl_plus, 1, wx.LEFT|wx.RIGHT, 0)
        control_sizer.Add(ctrl_find, 1, wx.LEFT|wx.RIGHT, 0)
        control_panel.SetSizer(control_sizer)
        self.main_sizer.Add(control_panel)
        return (control_panel, control_sizer, )
        

    def on_plus_button(self, event):
        self.listbox.add_item("New item (click, type to alter)")

    def on_minus_button(self, event):
        item = self.listbox.GetFirstSelected()
        removal = []
        while item > -1:
            removal.append(item)
            #self.listbox.Select(item, 0)
            item = self.listbox.GetNextSelected(item)
        self.listbox.remove_items(removal)
        
    def on_find(self, event):
        conflist = []
        if self.conf_hook:
            self.conf_hook(conflist)
        else:
            with wxMarkDialogSelect(self,
                            [ MarkViewItem(item, lambda x: x) for item in self.table ],
                            ret=conflist,
                            title="Select items") as conf:
                conf.ShowModal()
        for item in conflist:
            self.listbox.add_item(item)

    def set_conf(self, hook):
        self.conf_hook = hook

    def set_table(self, table):
        self.table = table

