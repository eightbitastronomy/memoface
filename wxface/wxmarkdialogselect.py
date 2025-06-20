import wx
from wxface.wxlistdialog import wxListDialog


class wxMarkDialogSelect(wxListDialog):

    def __init__(self, parent, table, **kwargs):
        wxListDialog.__init__(self,
                              parent,
                              table,
                              **kwargs)
        quick_panel = wx.Panel(self)
        self.main_sizer.Add(quick_panel, 0, wx.EXPAND, 0)
        quick_sizer = wx.BoxSizer(wx.HORIZONTAL)
        quick_label = wx.StaticText(quick_panel,
                                    wx.ID_ANY,
                                    label="Quick lookup:",
                                    style=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.ST_ELLIPSIZE_END)
        quick_enter_id = wx.NewId()
        self.quick_enter = wx.TextCtrl(quick_panel,
                                  quick_enter_id,
                                  value="",
                                  style=wx.TE_PROCESS_ENTER)
        label_x, label_y = quick_label.GetTextExtent("Quick lookup")
        quick_label.SetSize(wx.Size(label_x, label_y))
        entry_y = max(label_y, self.quick_enter.GetMinSize().y)
        entry_x = self.GetSize().x - label_x
        quick_sizer.Add(quick_label, 0, wx.CENTRE, 0)
        quick_sizer.Add(self.quick_enter, 1, wx.EXPAND, 0)
        self.quick_enter.Bind(wx.EVT_KEY_UP, lambda x: self.on_quick_scroll(x,self.quick_enter.GetValue()), self.quick_enter)
        quick_panel.SetSizer(quick_sizer)
        choice_panel = wx.Panel(self)
        self.main_sizer.Add(choice_panel, 0, wx.EXPAND, 0)
        choice_sizer = wx.BoxSizer(wx.HORIZONTAL)
        choice_logic = wx.StaticText(choice_panel,
                                     wx.ID_ANY,
                                     label="Select files with...",
                                     style=wx.ALIGN_LEFT | wx.ALIGN_CENTRE_VERTICAL | wx.ST_ELLIPSIZE_END)
        choice_sizer.Add(choice_logic, 0, wx.CENTRE, 0) #wx.ALIGN_CENTRE|wx.LEFT|wx.RIGHT|wx.TOP, 5)
        self.add_standard_buttons("Cancel",
                                  "Select",
                                  (choice_panel, choice_sizer,))
        self.quick_enter.SetFocus()

    def on_okay(self, event):
        #if self.conf_hook:
        #    for i in self.selection:
        #        self.selection.remove(i)
        #    item = self.listbox.GetFirstSelected()
        #    while item > -1:
        #        #dprint(3, "\nwxMarkDialog::Search::Item is " + str(item))
        #        buf = self.listbox.GetItem(item)
        #        #dprint(3, " index " + str(buf.Data))
        #        self.selection.append(self.table[item])
        #        self.listbox.Select(item, 0)
        #        item = self.listbox.GetNextSelected(item)
        #    self.conf_hook(set(self.selection), logic)
        item = self.listbox.GetFirstSelected()
        while item > -1:
            buf = self.listbox.GetItem(item)
            self.ret.append(self.table[item].get())
            item = self.listbox.GetNextSelected(item)
        #self.SetReturnCode(0)
        self.EndModal(0)
        self.Destroy()

    def on_quick_scroll(self, event, word):
        if word == "":
            self.listbox.EnsureVisible(0)
        else:
            for i, item in enumerate(self.table):
                if item.txt().find(word, 0, len(word)) > -1:
                    self.listbox.EnsureVisible(i)
        event.Skip()
