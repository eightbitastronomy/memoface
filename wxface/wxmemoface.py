# there is currently no means by which the memoface can "refresh" the info it has
# from the memoserv. Either I can implement a refresh button, or make it so that
# every change of state leads to service call. Excess service calls can be a real
# problem if the database is huge.


import wx
from wxface.wxmarkview import wxMarkView, MarkViewItem
from wxface.filter import Filter
from wxface.wxsubpanelchooser import wxSubPanelChooser
from wxface.wxsubpanelquick import wxSubPanelQuick
from wxface.wxsubpanelcheck import wxSubPanelCheck
from wxface.facestate import FaceState
from wxface.wxfileconfdialog import wxFileConfDialog
from wxface.wxdataconfdialog import wxDataConfDialog
from wxface.wxmanager import wxManager
import os
import subprocess
import sys
import json


globalwidth = 480
globalheight = 240
globallive = True


if globallive:
    from wxface.servinterface import ServInterface
    

grep_opts = ("Use grep", "Case Sensitive", "Follow links",)

def get_toc():
    return [ "audio", "bash", "C++", "database", "debian", "fedora", "java", "kernel", "linux", "machine", "os", "python", "rust", "SQL", "terminal", "windows", "yum", "zbus" ]
    
def get_types():
    return [ "Text", "Image", "PDF", "Code" ]
    
def get_files():
    return [ "a.txt", "b.pdf", "cpp.txt", "debug.txt", "errno.txt", "fedora.txt", "gnuplot.txt", "help.doc", "iolib.pdf", "java.pdf" ]




class wxMemoFace(wx.Frame):

    '''MemoServ Frontend Client'''
    
    def __init__(self, **kwargs):
        self.conf = None
        with open("conf.face.json", "r") as confptr:
            self.conf = json.load(confptr)
        self.size = wx.Size(int(self.conf["x"]), int(self.conf["y"]))
        wx.Frame.__init__(self,
                        None,
                        title="Memobook",
                        size=self.size)
        self.Bind(wx.EVT_CLOSE,
                  lambda e: self.__quit(e),
                  self)
        self.serv = None
        if globallive:
            try:
                self.serv = ServInterface()
                self.serv.initialize()
            except Exception as e:
                with wx.MessageDialog(self,
                                "Error connecting to service: " + str(e),
                                caption="Error",
                                style=wx.OK | wx.CENTRE) as message:
                    message.ShowModal()
                self.Destroy()
                return
            finally:
                if self.serv.interface is None:
                    print("Failed to connect to memoserv. Exiting.")
                    self.Destroy()
                    return
        self.confchange = False
        self.selection = [] 
        self.toc_marks = []
        self.toc_types = []
        self.toc_files = []
        if globallive:
            self.get_content()
        self.dsize = wx.Size(globalwidth - self.GetClientSize().GetWidth(), 
                            globalheight - self.GetClientSize().GetHeight())
        self.state = FaceState.FNDFILE
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._ctrlp = wx.Panel(self)
        control_sizer = wx.BoxSizer(wx.VERTICAL)
        file_button_id = wx.NewId()
        file_button = wx.Button(self._ctrlp,
                                  file_button_id,
                                  "Find File")
        file_button.SetSize(file_button.GetBestSize())
        mark_button_id = wx.NewId()
        mark_button = wx.Button(self._ctrlp,
                                  mark_button_id,
                                  "Find Mark")
        mark_button.SetSize(mark_button.GetBestSize())
        type_button_id = wx.NewId()
        type_button = wx.Button(self._ctrlp,
                                type_button_id,
                                "Find Type")
        manage_button_id = wx.NewId()
        manage_button = wx.Button(self._ctrlp,
                                manage_button_id,
                                "Manage")
        refresh_button_id = wx.NewId()
        refresh_button = wx.Button(self._ctrlp,
                                refresh_button_id,
                                "Refresh")
        go_panel = wx.Panel(self._ctrlp)
        go_sizer = wx.BoxSizer(wx.HORIZONTAL)
        go_button_id = wx.NewId()
        go_button = wx.Button(go_panel,
                            go_button_id,
                            "Go")
        go_size_old = go_button.GetBestSize()
        go_size_new = wx.Size(go_size_old.GetWidth(), go_size_old.GetHeight()*2)
        go_button.SetMinSize(go_size_new)
        go_sizer.Add(go_button, flag=wx.ALIGN_BOTTOM)
        go_panel.SetSizer(go_sizer)
        control_sizer.Add(file_button, 0, wx.EXPAND, 0)
        control_sizer.Add(mark_button, 0, wx.EXPAND, 0)
        control_sizer.Add(type_button, 0, wx.EXPAND, 0)
        control_sizer.Add(manage_button, 0, wx.EXPAND, 0)
        control_sizer.Add(refresh_button, 0, wx.EXPAND, 0)
        control_sizer.AddStretchSpacer()
        control_sizer.Add(go_panel, 0, wx.EXPAND, 0)
        self.main_sizer.Add(self._ctrlp, 0, wx.EXPAND, 0)
        self._ctrlp.SetSizer(control_sizer)
        #self._mdp = wxSubPanelChooser(self, table=get_toc(), target="marks")
        if globallive:
            self._mdp = wxSubPanelChooser(self, 
                                        #table=self.serv.interface.Toc("mark").split(", "))
                                        table=self.toc_marks)
        else:
            self._mdp = wxSubPanelChooser(self, table=get_toc())
        self._mdp.set_selection(0)
        self._tdp_dyn = wx.Panel(self)
        self._tdp_dyn_sizer = wx.BoxSizer(wx.VERTICAL)
        #self._tdp = wxSubPanelChooser(self._tdp_dyn, table=get_types(), target="types")
        if globallive:
            self._tdp = wxSubPanelChooser(self._tdp_dyn,
                                        #table=self.serv.interface.Toc("type").split(", "))
                                        table=self.toc_types)
        else:
            self._tdp = wxSubPanelChooser(self._tdp_dyn, table=get_types())
        self._tdp.set_selection(0)
        self.initial_select = True
        #self._fdp = wxSubPanelChooser(self, table=get_files(), target="files")
        if globallive:
            self._fdp = wxSubPanelChooser(self, 
                                        #table=self.serv.interface.Toc("file").split(", "))
                                        table=self.toc_files)
        else:
            self._fdp = wxSubPanelChooser(self, table=get_files())
        self._grep = wxSubPanelCheck(self._tdp_dyn, ("Use grep", "Case Sensitive", "Follow links",), title="Grep options:")
        self._grep.SetSize(self._grep.GetBestSize())
        self._tdp_dyn_sizer.Add(self._tdp, 1, wx.EXPAND, 0)
        self._tdp_dyn_sizer.Add(self._grep, 0, wx.EXPAND, 0)
        self._tdp_dyn_sizer.AddSpacer(5)
        self._tdp_dyn.SetSizer(self._tdp_dyn_sizer)
        self.main_sizer.Add(self._mdp, 0, wx.EXPAND, 0)
        self.main_sizer.Add(self._fdp, 0, wx.EXPAND, 0)
        #self.main_sizer.Add(self._tdp, 0, wx.EXPAND, 0)
        #self.main_sizer.Add(self._grep, 0, wx.EXPAND, 0)
        self.main_sizer.Add(self._tdp_dyn, 0, wx.EXPAND, 0)
        self.Bind(wx.EVT_BUTTON, lambda e: self.swap_dialog(self._mdp, self._tdp, self._fdp, FaceState.FNDFILE), file_button, file_button_id)
        self.Bind(wx.EVT_BUTTON, lambda e: self.swap_dialog(self._fdp, self._tdp, self._mdp, FaceState.FNDMARK), mark_button, mark_button_id)
        self.Bind(wx.EVT_BUTTON, lambda e: self.swap_dialog(self._mdp, self._fdp, self._tdp, FaceState.FNDTYPE), type_button, type_button_id)
        self.Bind(wx.EVT_BUTTON, lambda e: self.go(), go_button, go_button_id)
        self.Bind(wx.EVT_SIZE, lambda e: self.resize(e.GetSize()))
        self.Bind(wx.EVT_BUTTON, lambda e: self.spawn_manager(), manage_button, manage_button_id)
        self.Bind(wx.EVT_BUTTON, lambda e: self.content_refresh(), refresh_button, refresh_button_id)
        #self._mdp = mark_dialog_panel
        #self._fdp = file_dialog_panel
        #self._tdp = type_dialog_panel
        self.SetSizer(self.main_sizer)
        self._fdp.Hide()
        #self.SetSize(self.GetBestSize())
        self.Show()
                
        
    def swap_dialog(self, panel1, panel2, exitpanel, state):
        exitpanel.Hide()
        self.state = state
        if state == FaceState.FNDFILE:
            self._grep.Show()
            self.resize(self.GetSize())
            if self.initial_select:
                self._mdp.set_selection(0)
                self._tdp.set_selection(0)
        else:
            self._grep.Hide()
            if self.initial_select:
                self.initial_select = False
                self._tdp.set_selection(-1)
                self._mdp.set_selection(-1)
                self._fdp.set_selection(-1)
        panel1.Show()
        panel2.Show()
        self.main_sizer.Layout()
        
     
    def recalculate_self_size(self):
        globalx = self.size.GetWidth()
        dx = self.dsize.GetWidth()
        globaly = self.size.GetHeight()
        newsize = None
        match self.state:
            case FaceState.FNDFILE:
                x = ( 
                        self._mdp.GetBestSize().GetWidth() 
                        + self._tdp_dyn.GetBestSize().GetWidth() 
                        + self._ctrlp.GetBestSize().GetWidth() 
                        + dx
                )
            case FaceState.FNDMARK:
                x = (
                        self._mdp.GetBestSize().GetWidth() 
                        + self._ctrlp.GetBestSize().GetWidth() 
                        + dx
                )
            case FaceState.FNDTYPE:
                x = (
                        self._ctrlp.GetBestSize().GetWidth() 
                        + self._fdp.GetBestSize().GetWidth() 
                        + dx
                )
        return wx.Size(x,globaly)

    def swap_dialog2(self, panel1, panel2, exitpanel, state):
        exitpanel.Hide()
        self.state = state
        if state == FaceState.FNDFILE:
            self.resize(self.GetSize())
            self._grep.Show()
        else:
            self._grep.Hide()
            self.resize(self.GetSize())
        panel1.Show()
        panel2.Show()
        self.main_sizer.Layout()
        

    def resize(self, size):
        self.size = size
        self.conf["x"] = size.GetWidth()
        self.conf["y"] = size.GetHeight()
        self.confchange = True
        self.SetSize(size)
        #match self.state:
        #    case FaceState.FNDFILE:
        #        panelsize = wx.Size(int((size.GetWidth()-self._ctrlp.GetSize().GetWidth())/2),int(size.GetHeight()))
        #    case FaceState.FNDMARK:
        #        panelsize = wx.Size(self.size.GetWidth()-self._ctrlp.GetSize().GetWidth(), self.Size.GetHeight())
        #    case FaceState.FNDTYPE:
        #        panelsize = wx.Size(self.size.GetWidth()-self._ctrlp.GetSize().GetWidth(), self.Size.GetHeight())
        panelsize = wx.Size(int((size.GetWidth()-self._ctrlp.GetSize().GetWidth())/2),int(size.GetHeight()))
        self._mdp.SetMinSize(panelsize)
        self._fdp.SetMinSize(panelsize)
        self._tdp_dyn.SetMinSize(panelsize)
        self.Layout()
        
        
    def go(self):
        match self.state:
            case FaceState.FNDFILE:
                self.go_fndfile()
                return
            case FaceState.FNDMARK:
                self.go_fndother(self.state)
                return
            case FaceState.FNDTYPE:
                self.go_fndother(self.state)
                return
                
                
    def go_fndfile(self, **kwargs):
        mark_selection = self._mdp.get_selection()
        #if not mark_selection:
        #    return
        type_selection = self._tdp.get_selection()
        #if not type_selection:
        #    return
        self.__file_search(mark=mark_selection,
                    marklogic=self._mdp.get_logic(),
                    type=type_selection,
                    typelogic=self._tdp.get_logic(),
                    grep=self._grep.get_value(grep_opts[1]),
                    case=self._grep.get_value(grep_opts[0]),
                    link=self._grep.get_value(grep_opts[2]))        
        #filterprep = (
        #    filterprep.add_marks(mark_selection)
        #    .set_logic("mark", self._mdp.get_logic())
        #    .add_types(type_selection)
        #    .set_logic("type", self._tdp.get_logic())
        #    .set_grep_case(self._grep.get_value(grep_opts[0]))
        #    .set_grep_link(self._grep.get_value(grep_opts[2]))
        #    .set_grep_option(self._grep.get_value(grep_opts[1]))
        #    .set_equality("file")
        #)
        #if globallive:
        #    response = self.call_backend_search(filterprep.form())
        #else:
        #    response = self.call_backend_dummyFILE(filterprep.form())
        #print(response)
        #if not response:
        #    with wx.MessageDialog(self,
        #                        "No matches found",
        #                        caption="Search results",
        #                        style=wx.OK | wx.CENTRE) as message:
        #        message.ShowModal()
        #    return []
        #conflist = []
        #res = 0
        #with wxFileConfDialog(
        #        self,
        #        [ MarkViewItem(item, lambda x: str(os.path.basename(x)) + "  (" + str(os.path.dirname(x)) + ")") for item in response.split(", ") ],
        #        ret=conflist,
        #        title="Confirm file(s) to open") as conf:
        #    res = conf.ShowModal()        
        #match res:
        #    case -1:
        #        return
        #    case 0:
        #        self.launch(conflist)
        #        return
        #    case 1:
        #        self.launch(conflist)
        #        self.on_cancel(None)
        #        return
   
 
    def go_fndother(self, state):
        mark_selection = self._mdp.get_selection()
        file_selection = self._fdp.get_selection()
        type_selection = self._tdp.get_selection()
        if not (mark_selection or file_selection or type_selection):
            return
        if ((state == FaceState.FNDMARK) and file_selection and type_selection) or ((state == FaceState.FNDTYPE) and mark_selection and file_selection):
            with wx.MessageDialog(self,
                                "Cannot filter based on both criteria. Use one criterion and deselect all items from the second.",
                                caption="Search error",
                                style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        filterprep = Filter()
        response = None
        match state:
            case FaceState.FNDMARK:
                if file_selection:
                    filterprep = (
                        filterprep.add_files(file_selection)
                        .set_logic("file", self._fdp.get_logic())
                        .set_grep_case("false")
                        .set_grep_link("false")
                        .set_grep_option("false")
                        .set_equality("mark")
                    )
                else:
                    filterprep = (
                        filterprep.add_types(type_selection)
                        .set_logic("type", self._tdp.get_logic())
                        .set_grep_case("false")
                        .set_grep_link("false")
                        .set_grep_option("false")
                        .set_equality("mark")
                    )
                if globallive:
                    response = self.call_backend_search(filterprep.form())
                else:
                    response = self.call_backend_dummyMARK(filterprep.form())
            case FaceState.FNDTYPE:
                if file_selection:
                    filterprep = (
                        filterprep.add_files(file_selection)
                        .set_logic("file", self._fdp.get_logic())
                        .set_grep_case("false")
                        .set_grep_link("false")
                        .set_grep_option("false")
                        .set_equality("type")
                    )
                else:
                    filterprep = (
                        filterprep.add_marks(mark_selection)
                        .set_logic("mark", self._mdp.get_logic())
                        .set_grep_case("false")
                        .set_grep_link("false")
                        .set_grep_option("false")
                        .set_equality("type")
                    )
                if globallive:
                    response = self.call_backend_search(filterprep.form())
                else:
                    response = self.call_backend_dummyTYPE(filterprep.form())
        if not response:
            with wx.MessageDialog(self,
                            "No matches found",
                            caption="Search results",
                            style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        conflist = []
        res = 0
        with wxDataConfDialog(self,
                        [ MarkViewItem(item, lambda x: x) for item in response.split(", ") ],
                        ret=conflist,
                        title="Select data") as conf:
            res = conf.ShowModal()
        match res:
            case -1:
                return
            case 0:
                if state == FaceState.FNDMARK:
                    self.__file_search(mark=[e.txt() for e in conflist])
                else:
                    self.__file_search(type=[e.txt() for e in conflist])
                #self.launch(conflist)
                return
            case 1:
                #self.launch(conflist)
                return
    
    
    def __file_search(self, **kwargs):
        opt_grep = "false"
        opt_grepcase = "false"
        opt_greplink = "false"
        opt_mlogic = "or"
        opt_tlogic = "or"
        marks = None
        types = None
        filterprep = Filter()
        if "marklogic" in kwargs.keys():
            opt_mlogic = kwargs["marklogic"]
        if "typelogic" in kwargs.keys():
            opt_tlogic = kwargs["typelogic"]
        if "mark" in kwargs.keys():
            marks = kwargs["mark"]
            filterprep.add_marks(marks)
            filterprep.set_logic("mark", opt_mlogic)
        #else:
        #    return
        if "type" in kwargs.keys():
            types = kwargs["type"]
            filterprep.add_types(types)
            filterprep.set_logic("type", opt_tlogic)
        #else:   
        #    return
        if (marks is None) and (types is None):
            return
        if "grep" in kwargs.keys():
            opt_grep = kwargs["grep"]
        filterprep.set_grep_option(opt_grep)
        if "case" in kwargs.keys():
            opt_grepcase = kwargs["case"]
        filterprep.set_grep_case(opt_grepcase)
        if "link" in kwargs.keys():
            opt_greplink = kwargs["link"]
        filterprep.set_grep_link(opt_greplink)
        filterprep.set_equality("file")
        if globallive:
            response = self.call_backend_search(filterprep.form())
        else:
            response = self.call_backend_dummyFILE(filterprep.form())
        if not response:
            with wx.MessageDialog(self,
                                "No matches found",
                                caption="Search results",
                                style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return []
        conflist = []
        res = 0
        with wxFileConfDialog(
                self,
                [ MarkViewItem(item, lambda x: str(os.path.basename(x)) + "  (" + str(os.path.dirname(x)) + ")") for item in response.split(", ") ],
                ret=conflist,
                title="Confirm file(s) to open") as conf:
            res = conf.ShowModal()        
        match res:
            case -1:
                return
            case 0:
                self.launch(conflist)
                return
            case 1:
                self.launch(conflist)
                self.on_cancel(None)
                return


    def call_backend_search(self, request):
        return self.serv.search(request)
        
        
    def call_backend_dummyFILE(self, request):
        if sys.platform == "win32":
            return "C:\\Users\\migue\\help\\python\\notes_python3.txt, C:\\Users\\migue\\help\\rust\\rust_general.txt"
        else:
            return "/home/norfolk/help/python/notes_python3.txt, /home/norfolk/help/rust/rust_general.txt"
        #return []
       
        
    def call_backend_dummyMARK(self, request):
        return "code, rust, python, elisp, vimscript"

        
    def call_backend_dummyTYPE(self, request):
        return "Text, Code"
        
    
    def launch(self, list):
        #I suppose choice of application should happen here
        match sys.platform:
            case "win32":
                for item in list:
                    os.startfile(item.get())
            case "linux":
                for item in list:
                    #subprocess.run(["xdg-open", item.get()])
                    subprocess.Popen(["xdg-open", item.get()])


    def spawn_manager(self):
        mgr_window = wxManager(self,
                                serv=self.serv,
                                #size=self.size,
                                mark=get_toc(),
                                type=get_types())
        mgr_window.Show()


    def get_content(self):
        self.toc_marks = self.serv.interface.Toc("mark").split(", ") 
        self.toc_types = self.serv.interface.Toc("type").split(", ") 
        self.toc_files = self.serv.interface.Toc("file").split(", ") 


    def content_refresh(self):
        self.get_content()
        self._mdp.refresh(self.toc_marks)
        self._tdp.refresh(self.toc_types)
        self._fdp.refresh(self.toc_files)
        

    def on_cancel(self, event):
        self._ctrlp.Destroy()
        self._mdp.Destroy()
        self._fdp.Destroy()
        self._tdp_dyn.Destroy()
        self.Destroy()
        
    def send_search(self, searchfilter):
        pass


    def __quit(self, ev):
        if self.confchange:
            with open("conf.face.json", "w") as conffile:
                json.dump(self.conf, conffile, indent=4)
        ev.Skip()
