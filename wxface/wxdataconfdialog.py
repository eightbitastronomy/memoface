import wx
from wxface.wxlistdialog import wxListDialog
from wx import TheClipboard
from wx import TextDataObject



class wxDataConfDialog(wxListDialog):

    def __init__(self, parent, table, **kwargs):
        wxListDialog.__init__(self,
                              parent,
                              table,
                              **kwargs)
        choice_panel = wx.Panel(self)
        self.main_sizer.Add(choice_panel, 0, wx.EXPAND, 0)
        choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_standard_buttons("Cancel",
                                  "Select",
                                  (choice_panel, choice_sizer,))
        choice_clipboard = wx.Button(choice_panel,
                               wx.ID_ANY,
                               "Copy to Clipboard")
        self.Bind(wx.EVT_BUTTON, self.on_clipboard, choice_clipboard)
        choice_clipboard.SetSize(choice_clipboard.GetBestSize())
        choice_sizer.Add(choice_clipboard, 1, wx.EXPAND, 0)
        

    def on_clipboard(self, event):
        #dprint(3, "\nwxMarkConfDialog::on_clipboard")
        selection = []
        item = self.listbox.GetFirstSelected()
        while item > -1:
            buf = self.listbox.GetItem(item)
            selection.append(self.table[item].get())
            item = self.listbox.GetNextSelected(item)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(" ".join(selection)))
            wx.TheClipboard.Close()
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
