import wx
from wxface.wxlistdialog import wxListDialog



class wxFileConfDialog(wxListDialog):

    def __init__(self, parent, table, **kwargs):
        wxListDialog.__init__(self,
                              parent,
                              table,
                              **kwargs)
        choice_panel = wx.Panel(self)
        self.main_sizer.Add(choice_panel, 0, wx.EXPAND, 0)
        choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_standard_buttons("Cancel",
                                  "Open",
                                  (choice_panel, choice_sizer,))
        choice_o_and_q = wx.Button(choice_panel,
                               wx.ID_ANY,
                               "Open and Quit")
        self.Bind(wx.EVT_BUTTON, self.on_open_quit, choice_o_and_q)
        choice_o_and_q.SetSize(choice_o_and_q.GetBestSize())
        choice_sizer.Add(choice_o_and_q, 1, wx.EXPAND, 0)
        

    def on_open_quit(self, event):
        #dprint(3, "\nwxMarkConfDialog::on_open_quit")
        item = self.listbox.GetFirstSelected()
        while item > -1:
            buf = self.listbox.GetItem(item)
            self.ret.append(self.table[item])
            item = self.listbox.GetNextSelected(item)
        #self.SetReturnCode(1)
        self.EndModal(1)
        self.Destroy()

    def on_okay(self, event):
        #dprint(3, "\nwxMarkConfDialog::on_[okay|open]")
        #for item in self.selection:
        #    self.ret.append(item)
        #for i in self.selection:
        #    self.selection.remove(i)
        item = self.listbox.GetFirstSelected()
        while item > -1:
            buf = self.listbox.GetItem(item)
            self.ret.append(self.table[item])
            item = self.listbox.GetNextSelected(item)
        #self.SetReturnCode(0)
        self.EndModal(0)
        self.Destroy()
