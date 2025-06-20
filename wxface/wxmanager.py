import wx
import json
import os
from wxface.wxfilefielder import wxFileFielder
from wxface.wxitemadder import wxItemAdder
from wxface.facestate import FaceState
from wxface.wxfileloader import wxFileLoader
from wxface.wxfilefilterer import wxFileFilterer
from wxface.wxitemfilterer import wxItemFilterer
from wxface.wxitemchooser import wxItemChooser
from wxface.wxconfigurepanel import wxConfigurePanel
from wxface.modifier import Modifier
from wxface.manager import Manager



def get_fake_marks():
    return ["python", "python3", "scripting", "coding"]
    
def get_fake_types():
    return ["Text", "Code"]
    
def get_fake_dirs():
    return ["C:\\users\\migue", "C:\\users\\migue\\help", "C:\\users\\migue\\code"]
    
def get_fake_backups():
    return ["backup_0000", "backup_0001", "backup_0002", "backup_0003"]

toggler = True

def test_server():
    global toggler
    return toggler

def start_server():
    global toggler
    toggler = True

def stop_server():
    global toggler
    toggler = False


class wxManager(wx.Frame):
    
    
    def __init__(self, parent, **kwargs):
        self.serv = None
        if "serv" in kwargs.keys():
            self.serv = kwargs["serv"]
        if "size" in kwargs.keys():
            self.size = kwargs["size"]
        else:
            self.size = wx.Size(480, 320)
        self.table_marks = []
        if "mark" in kwargs.keys():
            self.table_marks = kwargs["mark"]
        self.table_types = []
        if "type" in kwargs.keys():
            self.table_types = kwargs["type"]
        wx.Frame.__init__(self,
                        parent,
                        title="Manage MemoServ",
                        size=self.size)
        self.__apply_hook = self.apply_add_rec
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self._modep = wx.Panel(self)
        mode_sizer = wx.BoxSizer(wx.VERTICAL)
        add_record_id = wx.NewId()
        self._add_record_btn = wx.Button(self._modep,
                                        add_record_id,
                                        "Add record")
        self.Bind(wx.EVT_BUTTON, 
                lambda e: self.display_add_record(e) and self.set_apply_hook(self.apply_add_rec),
                self._add_record_btn)
        mod_record_id = wx.NewId()
        self._mod_record_btn = wx.Button(self._modep,
                                        mod_record_id,
                                        "Modify record")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.display_mod_record(e) and self.set_apply_hook(self.apply_mod_rec),
                self._mod_record_btn)
        rem_record_id = wx.NewId()
        self._rem_record_btn = wx.Button(self._modep,
                                        rem_record_id,
                                        "Remove record")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.display_rem_record(e) and self.set_apply_hook(self.apply_rem_rec),
                self._rem_record_btn)
        import_id = wx.NewId()
        self._import_btn = wx.Button(self._modep,
                                    import_id,
                                    "Import")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.display_import(e) and self.set_apply_hook(self.apply_import),
                self._import_btn)
        export_id = wx.NewId()
        self._export_btn = wx.Button(self._modep,
                                    export_id,
                                    "Export")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.display_export(e) and self.set_apply_hook(self.apply_export),
                self._export_btn)
        backup_id = wx.NewId()
        self._backup_btn = wx.Button(self._modep,
                                    backup_id,
                                    "Backup")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.display_backup(e) and self.set_apply_hook(self.apply_backup),
                self._backup_btn)
        config_id = wx.NewId()
        self._config_btn = wx.Button(self._modep,
                                    config_id,
                                    "Configure")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.display_general(e) and self.set_apply_hook(self.apply_general),
                self._config_btn)
        quit_id = wx.NewId()
        self._toggle_btn = wx.Button(self._modep,
                                        quit_id,
                                        "Stop/Start")
        self.Bind(wx.EVT_BUTTON,
                lambda e: self.server_toggle(e),
                self._toggle_btn)
        mode_sizer.Add(self._add_record_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._mod_record_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._rem_record_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._import_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._export_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._backup_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._config_btn, 0, wx.EXPAND, 1)
        mode_sizer.Add(self._toggle_btn, 0, wx.EXPAND, 1)
        self._applyp = wx.Panel(self._modep)
        apply_sizer = wx.BoxSizer(wx.HORIZONTAL)
        apply_button_id = wx.NewId()
        # Initial hook for apply button will be for Add-Record mode
        apply_button = wx.Button(self._applyp,
                                apply_button_id,
                                "Apply")
        self.Bind(wx.EVT_BUTTON, lambda e: self.__apply_hook(self.confirm), apply_button, apply_button_id)
        apply_size_old = apply_button.GetBestSize()
        apply_size_new = wx.Size(apply_size_old.GetWidth(), apply_size_old.GetHeight()*2)
        apply_button.SetMinSize(apply_size_new)
        apply_sizer.Add(apply_button, flag=wx.ALIGN_BOTTOM)
        self._applyp.SetSizer(apply_sizer)
        mode_sizer.AddStretchSpacer()
        mode_sizer.Add(self._applyp, 0, wx.EXPAND, 1)
        self._modep.SetSizer(mode_sizer)
        self._workp = wx.Panel(self)
        work_sizer = wx.BoxSizer(wx.VERTICAL)
        # Add Record
        self._file = wxFileFielder(self._workp)
        self._mark = wxItemAdder(self._workp, 
                                self.table_marks,
                                label="Mark(s):",
                                width=wx.Size(self.size.GetWidth(), 
                                    int((self.size.GetHeight()-self._modep.GetSize().GetHeight())/2)))
        self._type = wxItemAdder(self._workp,
                                self.table_types,
                                label="Type(s):",
                                width=wx.Size(self.size.GetWidth(), 
                                    int((self.size.GetHeight()-self._modep.GetSize().GetHeight())/2)))
        # Modify Record
        self._fileloader = wxFileLoader(self._workp)
        self._fileloader.Hide()
        self._markmod = wxItemAdder(self._workp,
                                self.table_marks,
                                label="Available Mark(s):",
                                width=wx.Size(self.size.GetWidth(),
                                    int((self.size.GetHeight()-self._modep.GetSize().GetHeight())/2)),
                                mode="modify",
                                tocright=get_fake_marks(),
                                labelright="Existing Mark(s):")
        self._markmod.Hide()
        self._typemod = wxItemAdder(self._workp,
                                self.table_types,
                                label="Available Type(s):",
                                width=wx.Size(self.size.GetWidth(),
                                    int((self.size.GetHeight()-self._modep.GetSize().GetHeight())/2)),
                                mode="modify",
                                tocright=get_fake_types(),
                                labelright="Existing Type(s):")
        self._typemod.Hide()
        # Remove Record
        self._rem_label = wx.StaticText(self._workp,
                                        wx.ID_ANY,
                                        label = "Include?",
                                        style = wx.LEFT)
        self._rem_label.Hide()
        self._rem_filef = wxFileFilterer(self._workp)
        self._rem_filef.Hide()
        self._rem_markf = wxItemFilterer(self._workp,
                                        self.table_marks,
                                        default="By Mark:")
        self._rem_markf.Hide()
        self._rem_typef = wxItemFilterer(self._workp,
                                        self.table_types,
                                        default="By Type:")
        self._rem_typef.Hide()
        self._rem_warn = wx.StaticText(self._workp,
                                        wx.ID_ANY,
                                        label = "Removals must match all selected criteria.",
                                        style = wx.LEFT)
        self._rem_warn.Hide()
        # Import
        #   using _fileloader for import file
        backupinfo = json.loads(self.serv.interface.Repositories())
        includes = []
        excludes = []
        if backupinfo:
            #print(backupinfo)
            includes = backupinfo["include"]
            excludes = backupinfo["exclude"]
        else:
            includes = get_fake_dirs()
            excludes = get_fake_dirs()
        self._import_log = wxFileLoader(self._workp, mode="save", label="Log file:")
        self._import_log.Hide()
        self._import_incl = wxItemChooser(self._workp,
                                        #[ MarkViewItem(item, lambda x: x) for item in get_fake_dirs() ],
                                        table=includes,
                                        label="Folders included:",
                                        labelleft="Find folders")
        self._import_incl.Hide()
        self._import_opt_link = wx.CheckBox(self._workp,
                                        label="Follow symbolic links",
                                        id=wx.ID_ANY)
        self._import_opt_link.SetValue(False)
        self._import_opt_link.Hide()
        self._import_excl = wxItemChooser(self._workp,
                                        #[ MarkViewItem(item, lambda x: x) for item in get_fake_dirs() ],
                                        table=excludes,
                                        label="Folders excluded:",
                                        labelleft="Find folders")
        self._import_excl.Hide()
        # Export
        self._export_loader = wxFileLoader(self._workp, mode="save")
        self._export_loader.Hide()
        # Configure Backups
        self._backup = wxConfigurePanel(self._workp,
                                        descr="Configuration for backup:",
                                        text=[
                                                ("freq","Frequency (days):","1",),
                                                ("mult", "Number of backups:", "4"),
                                                ("base", "Base name for files:", "backup_")
                                            ],
                                        dir=[
                                                ("loc", "Location of backups:", "C:\\Users\\migue"),
                                            ],
                                        check=[
                                                ("force", "Force backup now?"),
                                                ("remove", "Remove existing backups?"),
                                            ],
                                        list=[
                                                (   
                                                    "load",
                                                    "Load backup now?",
                                                    "Select a file:",
                                                    get_fake_backups()
                                                ),
                                            ]
                                        )
        self._backup.Hide()
        # Configure General
        #self._general = wxConfigurePanel(self._workp,
        #                                descr="General Options:",
        #                                check=[
        #                                        ("quit", "Shutdown MemoServ now?"),
        #                                    ]
        #                                )
        #self._general.Hide()
        # Finish up
        work_sizer.Add(self._file, 0, wx.EXPAND, 0)
        work_sizer.Add(self._mark, 0, wx.EXPAND, 0)
        work_sizer.Add(self._type, 0, wx.EXPAND, 0)
        work_sizer.Add(self._fileloader, 0, wx.EXPAND, 0)
        work_sizer.Add(self._markmod, 0, wx.EXPAND, 0)
        work_sizer.Add(self._typemod, 0, wx.EXPAND, 0)
        work_sizer.Add(self._rem_label, 0, wx.LEFT, 0)
        work_sizer.Add(self._rem_filef, 0, wx.EXPAND, 0)
        work_sizer.Add(self._rem_markf, 0, wx.EXPAND, 0)
        work_sizer.Add(self._rem_typef, 0, wx.EXPAND, 0)
        work_sizer.Add(self._rem_warn, 0, wx.LEFT, 0)
        work_sizer.Add(self._import_log, 0, wx.EXPAND, 0)
        work_sizer.Add(self._import_opt_link, 0, wx.EXPAND, 0)
        work_sizer.Add(self._import_incl, 0, wx.EXPAND, 0)
        work_sizer.Add(self._import_excl, 0, wx.EXPAND, 0)
        work_sizer.Add(self._export_loader, 0, wx.EXPAND, 0)
        work_sizer.Add(self._backup, 0, wx.EXPAND, 0)
        #work_sizer.Add(self._general, 0, wx.EXPAND, 0)
        self._workp.SetSizer(work_sizer)
        self.main_sizer.Add(self._modep, 0, wx.EXPAND, 0)
        self.main_sizer.Add(self._workp, 2, wx.EXPAND, 0)
        self.SetSizer(self.main_sizer)
        self.SetSize(self.GetBestSize())
        self.Show()
    
        
    def display_add_record(self, e):
        self._fileloader.Hide()
        self._markmod.Hide()
        self._typemod.Hide()
        self._rem_label.Hide()
        self._rem_filef.Hide()
        self._rem_markf.Hide()
        self._rem_typef.Hide()
        self._rem_warn.Hide()
        self._import_log.Hide()
        self._import_opt_link.Hide()
        self._import_incl.Hide()
        self._import_excl.Hide()
        self._export_loader.Hide()
        self._backup.Hide()
        #self._general.Hide()
        self._file.Show()
        self._mark.Show()
        self._type.Show()
        self.__apply_hook = self.apply_add_rec
        self.main_sizer.Layout()
        return True
        
        
    def display_mod_record(self, e):
        self._import_log.Hide()
        self._import_opt_link.Hide()
        self._import_incl.Hide()
        self._import_excl.Hide()
        self._export_loader.Hide()
        self._backup.Hide()
        #self._general.Hide()
        self._rem_label.Hide()
        self._rem_filef.Hide()
        self._rem_markf.Hide()
        self._rem_typef.Hide()
        self._rem_warn.Hide()
        self._file.Hide()
        self._fileloader.Show()
        self._mark.Hide()
        self._markmod.Show()
        self._type.Hide()
        self._typemod.Show()
        self.__apply_hook = self.apply_mod_rec
        self.main_sizer.Layout()
        return True
        
        
    def display_rem_record(self, e):
        self._fileloader.Hide()
        self._markmod.Hide()
        self._typemod.Hide()
        self._file.Hide()
        self._mark.Hide()
        self._type.Hide()
        self._import_log.Hide()
        self._import_opt_link.Hide()
        self._import_incl.Hide()
        self._import_excl.Hide()
        self._export_loader.Hide()
        self._backup.Hide()
        #self._general.Hide()
        self._rem_label.Show()
        self._rem_filef.Show()
        self._rem_markf.Show()
        self._rem_typef.Show()
        self._rem_warn.Show()
        self.__apply_hook = self.apply_rem_rec
        self.main_sizer.Layout()
        return True
    
    
    def display_import(self, e):
        self._fileloader.Show()
        self._markmod.Hide()
        self._typemod.Hide()
        self._file.Hide()
        self._mark.Hide()
        self._type.Hide()
        self._import_log.Show()
        self._import_opt_link.Show()
        self._import_incl.Show()
        self._import_excl.Show()
        self._rem_label.Hide()
        self._rem_filef.Hide()
        self._rem_markf.Hide()
        self._rem_typef.Hide()
        self._rem_warn.Hide()
        self._export_loader.Hide()
        self._backup.Hide()
        #self._general.Hide()
        self.__apply_hook = self.apply_import
        self.main_sizer.Layout()
        return True
    
    
    def display_export(self, e):
        self._fileloader.Hide()
        self._markmod.Hide()
        self._typemod.Hide()
        self._file.Hide()
        self._mark.Hide()
        self._type.Hide()
        self._import_log.Hide()
        self._import_opt_link.Hide()
        self._import_incl.Hide()
        self._import_excl.Hide()
        self._rem_label.Hide()
        self._rem_filef.Hide()
        self._rem_markf.Hide()
        self._rem_typef.Hide()
        self._rem_warn.Hide()
        self._backup.Hide()
        #self._general.Hide()
        self._export_loader.Show()
        self.__apply_hook = self.apply_export
        self.main_sizer.Layout()
        return True
    
    
    def display_backup(self, e):
        self._fileloader.Hide()
        self._markmod.Hide()
        self._typemod.Hide()
        self._file.Hide()
        self._mark.Hide()
        self._type.Hide()
        self._import_log.Hide()
        self._import_incl.Hide()
        self._import_excl.Hide()
        self._rem_label.Hide()
        self._rem_filef.Hide()
        self._rem_markf.Hide()
        self._rem_typef.Hide()
        self._rem_warn.Hide()
        self._export_loader.Hide()
        #self._general.Hide()
        self._backup.Show()
        self.__apply_hook = self.apply_backup
        self.main_sizer.Layout()
        return True
        
        
    def display_general(self, e):
        self._fileloader.Hide()
        self._markmod.Hide()
        self._typemod.Hide()
        self._file.Hide()
        self._mark.Hide()
        self._type.Hide()
        self._import_log.Hide()
        self._import_incl.Hide()
        self._import_excl.Hide()
        self._rem_label.Hide()
        self._rem_filef.Hide()
        self._rem_markf.Hide()
        self._rem_typef.Hide()
        self._rem_warn.Hide()
        self._export_loader.Hide()
        self._backup.Hide()
        #self._general.Show()
        self.__apply_hook = self.apply_general
        self.main_sizer.Layout()
        return True
    
    
    def set_apply_hook(self, func):
        self.__apply_hook = func
        return True


    def apply_add_rec(self, func):
        ready_files = self._file.get_files()
        ready_marks = self._mark.get()
        ready_types = self._type.get()
        if (ready_files == []) or (ready_marks == []) or (ready_types == []):
            with wx.MessageDialog(self,
                                    "All fields must have values for a record to be added.",
                                    caption="Add Record",
                                    style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        #here, check that the files are indeed located in a repo-include directory.
        #if not, confirm whether they are to be added anyway.
        if not self.check_for_repo_inclusion(ready_files):
            return
        if func("addition of record") == wx.ID_OK:
            for filename in ready_files:
                addmodifier = Modifier()
                addmodifier.mode_add_record()
                addmodifier.set_files([filename])
                addmodifier.set_types(ready_types)
                addmodifier.set_marks(ready_marks)
                self.serv.interface.Modify(addmodifier.form())
            ###debug output
            print("add record: files are " + str(ready_files))
            print("add record: marks are " + str(ready_marks))
            print("add record: types are " + str(ready_types))
            # dialog/notification box on successful add
    
    
    def apply_mod_rec(self, func):
        ready_files = list(filter(None, self._fileloader.get_file()))
        ready_marks = list(filter(None, self._markmod.get()))
        ready_types = list(filter(None, self._typemod.get()))
        if (ready_files == []) or (ready_marks == []) or (ready_types == []):
            with wx.MessageDialog(self,
                                    "All fields must have values for a record to be added.",
                                    caption="Add Record",
                                    style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        # MemoServ needs a call that says what will be removed and what will be added...
        # ...Hence, need to take the results of get() and pass to a method with the old lists,
        # ...then process into rem's and add's, returning a single piece of the call
        # So, process(oldmarks, newmarks) might return "mark add 1 this rem 2 that then" e.g.
        if func("modification of this record") == wx.ID_OK:
            ###debug output
            print("mod record: file is " + str(ready_files))
            print("mod record: marks are " + str(ready_marks))
            print("mod record: types are " + str(ready_types))
            if self.serv:
                adder = Modifier()
                adder.mode_add_record()
                adder.set_files(ready_files)
                adder.set_marks(ready_marks)
                adder.set_types(ready_types)
                self.serv.interface.Modify(adder.form())
    
    
    def apply_rem_rec(self, func):
        ready_files = []
        ready_marks = []
        ready_types = []
        temptotalchecks = 0
        tempmultiflag = False
        if self._rem_filef.is_checked():
            temptotalchecks += 1
            ready_files = self._rem_filef.get_files()
            if len(ready_files) > 1:
                tempmultiflag = True
        if self._rem_markf.is_checked():
            temptotalchecks += 1
            ready_marks = self._rem_markf.get_selection()
            if len(ready_files) > 1:
                tempmultiflag = True
        if self._rem_typef.is_checked():
            temptotalchecks += 1
            ready_types = self._rem_typef.get_selection()
            if len(ready_files) > 1:
                tempmultiflag = True
        if temptotalchecks != 1:
            with wx.MessageDialog(self,
                                    "Under construction: only one criterion may be applied at a time.",
                                    caption="Remove Record",
                                    style=wx.OK | wx.CENTRE) as messtotal:
                messtotal.ShowModal()
            return
        if tempmultiflag:
            with wx.MessageDialog(self,
                                    "Under construction: select only one value from the list.",
                                    caption="Remove Record",
                                    style=wx.OK | wx.CENTRE) as messnumval:
                messnumval.ShowModal()
            return
        if (ready_files == []) and (ready_marks == []) and (ready_types == []):
            with wx.MessageDialog(self,
                                    "At least one search parameter is required for a record to be removed.",
                                    caption="Remove Record",
                                    style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        else:
            if func("removal of any applicable records") == wx.ID_OK:
            # If a field is checked but selection is empty, drop from the filter
                remover = Modifer()
                remover.mode_target_remove()
                if ready_files:
                    remover.set_field("file")
                    remover.set_fieldtarg(ready_files[0])
                    ###debug output
                    print("File filter: " + str(ready_files))
                if ready_marks:
                    remover.set_field("mark")
                    remover.set_fieldtarg(ready_marks[0])
                    ###debug output
                    print("Mark filter: " + str(ready_marks))
                if ready_types:
                    remover.set_field("type")
                    remover.set_files(ready_types[0])
                    ###debug output
                    print("Type filter: " + str(ready_types))
                self.serv.interface.Modify(remover.form())
        return
        
        
    def apply_import(self, func):
        ready_file = ""
        ready_log = ""
        ready_incl = []
        ready_excl = []
        ready_file = self._fileloader.get_file()
        ready_log = self._import_log.get_file()
        ready_incl = self._import_incl.get_all()
        ready_excl = self._import_excl.get_all()
        # behavior: if not includes or excludes are chosen, the include directory will be the
        #   present working directory.
        if (ready_file == "" or ready_file == None) or (ready_log == "" or ready_log == None):
            with wx.MessageDialog(self,
                                "An import file and log file must be chosen.",
                                caption="Import",
                                style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        # prepare confirmation dialog
        dialog = ""
        if ready_incl == []:
            with wx.MessageDialog(self,
                                "An include folder must be chosen.",
                                caption="Import",
                                style=wx.OK | wx.CENTRE) as msg_inc:
                msg_inc.ShowModal()
            return
        else:
            dialog = "Confirm import with include folders of "
            for fldr in ready_incl:
                dialog += fldr + ", "
        if func(dialog) == wx.ID_OK:
            repomgr = Manager()
            repomgr.mode_set_repo()
            repomgr.set_includes(ready_incl)
            repomgr.set_excludes(ready_excl)
            self.serv.interface.Manage(repomgr.form())
            importer = Manager()
            importer.mode_import()
            importer.set_path(ready_file)
            importer.set_log(ready_log)
            importer.set_link(self._import_opt_link.GetValue)
            self.serv.manage_wait(importer.form(),720)
        ###debug output
        print("Import file: " + ready_file)
        print("Import log: " + ready_log)
        print("Import includes: " + str(ready_incl))
        print("Import excludes: " + str(ready_excl))
        return
        
        
    def apply_export(self, func):
        ready_file = self._export_loader.get_file()
        if ready_file == "":
            with wx.MessageDialog(self,
                                "An export file must be chosen",
                                caption="Export",
                                style=wx.OK | wx.CENTRE) as message:
                message.ShowModal()
            return
        ###debug output
        print("export file: " + ready_file)
        if self.serv:
            mgr = Manager()
            mgr.mode_export()
            mgr.set_log(ready_file)
            self.serv.interface.Manage(mgr.form())
        return


    def apply_backup(self, func):
        ready_freq = -1
        tmp_freq = self._backup.get_txt_value("freq")
        tmp_mult = self._backup.get_txt_value("mult")
        tmp_base = self._backup.get_txt_value("base")   # removing whitespace while leaving intended (escaped) whitespace
                                                        # requires thought and maybe a function implementing regex
        tmp_loc = self._backup.get_dir_value("loc")
        tmp_force_load = self._backup.get_check_box("force")
        tmp_remove_exist = self._backup.get_check_box("remove")
        tmp_load_now = self._backup.get_check_list("load")
        if (not tmp_freq.isnumeric()) or (not tmp_mult.isnumeric()):
            with wx.MessageDialog(self,
                                "Improper numeric values used in text fields",
                                caption="Format error",
                                style=wx.OK | wx.CENTRE) as message_num:
                message_num.ShowModal()
            return
        if tmp_loc is None:
            with wx.MessageDialog(self,
                                "Backup location may not be left blank",
                                caption="Format error",
                                style=wx.OK | wx.CENTRE) as message_loc:
                message_loc.ShowModal()
            return
        if tmp_load_now == "%INVALIDSELECTION%":
            with wx.MessageDialog(self,
                                "Either select a backup to load or uncheck the option",
                                caption="Option error",
                                style=wx.OK | wx.CENTRE) as message_load:
                message_load.ShowModal()
            return
        ###debug output
        print("freq: " + tmp_freq)
        print("mult: " + tmp_mult)
        print("base: " + tmp_base)
        print("loc: " + tmp_loc)
        if tmp_force_load:
            print("Backup now? Yes")
        else:
            print("Backup now? No")
        if tmp_remove_exist:
            print("Remove backups? Yes")
        else:
            print("Remove backups? No")
        if tmp_load_now:
            print("Load file " + tmp_load_now)
        else:
            print("Do not load a file.")
        return
        
        
    def apply_general(self, func):
        #tmp_quit = self._general.get_check_box("quit")
        #if tmp_quit:
        #    print("Shut down")
        #else:
        #    print("Do not shut down")
        return

    
    def confirm(self, text):
        with wx.MessageDialog(self,
                                "Please confirm " + text + ":",
                                caption="Confirmation",
                                style=wx.OK |  wx.CANCEL | wx.CANCEL_DEFAULT | wx.CENTRE) as message:
            message.SetOKLabel("Confirm")
            return message.ShowModal()
    
    
    def server_toggle(self, event):
        if test_server():
            stop_server()
        else:
            start_server()
        ###debug output
        print("Server is running? " + str(test_server()))


    def check_for_repo_inclusion(self, filelist):
        includes = self._import_incl.get_all() # this probably need changed
        excludes = self._import_excl.get_all()
        flagged = []
        for item in filelist:
            good_so_far = True
            path = os.sep.join(os.path.realpath(item).split(os.sep)[:-1])
            for exclusion in excludes:
                if is_subdir_of(path, exclusion):
                    flagged.append(item)
                    good_so_far = False
                    break
            if good_so_far:
                # only reached if was not in an exclude dir, so check for include dirs
                good_so_far = False
                for inclusion in includes:
                    if is_subdir_of(path, inclusion):
                        good_so_far = True
                        break
            else:
                # only reached if path was in an excluded dir
                continue
            if not good_so_far:
                # only reached if path was neither excluded nor included
                flagged.append(item)
        if flagged:
            # dialog for confirmation
            beginning = "The following files are not located in included directories for the MemoServ repositories:\n"
            filestring = "\n".join(flagged)
            ending = "\nPlease confirm the addition of these files."
            with wx.MessageDialog(self,
                                beginning + filestring + ending,
                                caption="Confirmation",
                                style=wx.OK |  wx.CANCEL | wx.CANCEL_DEFAULT | wx.CENTRE) as message:
                message.SetOKLabel("Confirm")
                if message.ShowModal() == wx.ID_OK:
                    return True # the addrecord routine will continue
                else:
                    return False # the addrecord routine will be canceled
        else:
            return True # the addrecord routine will continue


def is_subdir_of(testpath, refpath):
    reflist = os.path.realpath(refpath).split(os.sep)
    testlist = os.path.realpath(testpath).split(os.sep)
    for i in range(0, len(reflist)):
        if testlist[i] != reflist[i]:
            return False
    return True
