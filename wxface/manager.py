from enum import Enum
from wxface.commutility import build_single


class MgrMode(Enum):
    NULL = 0
    IMPORT = 1
    EXPORT = 2
    SETSRC = 3
    SETRPO = 4
    SETRPT = 5
    MODRPO = 6


class Manager:


    def __init__(self):
        self.mode = MgrMode.NULL
        self.path = None
        self.path_inc = None
        self.path_exc = None
        self.log = None
        self.opt_link = "false"


    def mode_import(self):
        self.mode = MgrMode.IMPORT


    def mode_export(self):
        self.mode = MgrMode.EXPORT


    def mode_set_repo(self):
        self.mode = MgrMode.SETRPO

    
    def mode_set_source(self):
        self.mode = MgrMode.SETSRC


    def mode_set_repo_trunk(self):
        self.mode = MgrMode.SETRPT


    def mode_mod_repo(self):
        self.mode = MgrMode.MODRPO


    def set_trunk(self, tr):
        self.path = tr


    def set_path(self, pth):
        self.path = pth


    def set_includes(self, paths):
        self.path_inc = paths


    def set_excludes(self, paths):
        self.path_exc = paths


    def set_log(self, path):
        self.log = path


    def set_link(self, opt):
        if opt == True:
            self.opt_link = "true"
        else:
            self.opt_link = "false"


    def form(self):
        running = []
        match self.mode:
            case MgrMode.NULL:
                return []
            case MgrMode.IMPORT:
                if self.path and self.log:
                    running = ["import", "6", "source", self.path, "log", self.log, "link", self.opt_link]
            case MgrMode.EXPORT:
                if self.log:
                    running = ["export", "1", self.log]
            case MgrMode.SETSRC:
                return []
            case MgrMode.SETRPO:
                if self.path_inc:
                    running.extend(build_single("include", None, self.path_inc))
                if self.path_exc:
                    running.extend(build_single("exclude", None, self.path_exc))
                if self.opt_link:
                    running.extend(["link", self.opt_link])
                if running == []:
                    return []
                running.insert(0, str(len(running)))
                running.insert(0, "setrepo")
            case MgrMode.SETRPT:
                return []
            case MgrMode.MODRPO:
                return []
        return running
