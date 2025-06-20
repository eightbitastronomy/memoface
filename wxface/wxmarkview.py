import wx
import wx.lib.mixins.listctrl as listmix



class MarkViewItem:

    data = None
    string_f = None
    
    def __init__(self, item=None, sfunc=None):
        self.data = item
        self.string_f = sfunc

    def get(self):
        return self.data

    def txt(self):
        return self.string_f(self.data)
        

class wxMarkView(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):

    def __init__(self, parent, data, **kwargs):
        flags = wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_NO_HEADER
        if "single" in kwargs.keys():
            if kwargs["single"] == True:
                flags = flags | wx.LC_SINGLE_SEL
        wx.ListCtrl.__init__(self, 
                             parent,
                             style=flags)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.data = data
        self.view = None
        self.current = 0
        self.previous = -1
        self.InsertColumn(0, "Marks")
        self.SetColumnWidth(0, self.GetParent().GetClientSize().x)
        self.SetItemCount(len(data))
        self.setResizeColumn(0)
       
    def clear(self):
        self.DeleteAllItems()
        self.data = []

    def set_data(self, mvilist):
        self.data = mvilist
        self.SetItemCount(len(mvilist))
        self.Refresh()
 
    def Insert(self, item):
        if not item.txt() in [x.txt() for x in self.data]:
            self.data.append(item)
            self.SetItemCount(len(self.data))

    def SetSize(self, sz):
        self.SetColumnWidth(0, sz.x)
        wx.ListCtrl.SetSize(self, sz)

    def SetListView(self, outer):
        self.view = outer
 
    def OnGetItemText(self, item, col):
        return self.data[item].txt()

    def OnGetItemImage(self, item):
        return 0

    def OnGetItemAttr(self, item):
        return None

    def remove_selected(self):
        indices = []
        itemnum = self.GetFirstSelected()
        while itemnum > -1:
            indices.append(itemnum)
            itemnum = self.GetNextSelected(itemnum)
        for index in sorted(indices, reverse=True):
            self.data.pop(index)
        self.SetItemCount(len(self.data))
        if len(self.data) > 0:
            self.RefreshItems(0,len(self.data)-1)
