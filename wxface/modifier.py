from wxface.commutility import build_single
from enum import Enum


#def _form_single(term, termvec):
    #count = 0
#    result = []
#    result.append(term)
#    result.append(str(len(termvec)))
#    result.extend(termvec)
    #return " ".join(termvec)
#    return result



class ModMode(Enum):
    ADDREC = 0
    FIELDR = 1
    MARKUP = 2
    TARGRM = 3


class Modifier:


    def __init__(self):
        self.mod = ModMode.ADDREC
        self.markadd = []
        self.markrem = []
        self.types = []
        self.files = []
        self.field = ""
        self.fieldtarg = ""
        self.fieldnew = ""

    
    def mode_add_record(self):
        self.mod = ModMode.ADDREC
        return self


    def mode_field_replace(self):
        self.mod = ModMode.FIELDR
        return self


    def mode_mark_update(self):
        self.mod = ModMode.MARKUP
        return self


    def mode_target_remove(self):
        self.mod = ModMode.TARGRM
        return self


    def set_files(self, filevec):
        self.files = filevec
        return self


    def set_types(self, typevec):
        self.types = typevec
        return self


    def set_marks(self, markvec):
        self.markadd = markvec
        return self


    def set_mark_add(self, markvec):
        self.markadd = markvec
        return self


    def set_mark_rem(self, markvec):
        self.markrem = markvec
        return self


    def set_field(self, field):
        self.field = field
        return self


    def set_field_target(self, value):
        self.fieldtarg = value
        return self


    def set_field_new(self, value):
        self.fieldnew = value
        return self


    def form(self):
        runningvec = []
        match self.mod:
            case ModMode.ADDREC:
                if (len(self.markadd) < 1) or (len(self.types) < 1) or (len(self.files) < 1):
                    return []
                runningvec.extend(build_single("file", None, self.files))
                runningvec.extend(build_single("mark", None, self.markadd))
                runningvec.extend(build_single("type", None, self.types))
                runningvec.insert(0, str(len(runningvec)))
                runningvec.insert(0, "addrecord")
            case ModMode.FIELDR:
                if self.field and self.fieldtarg and self.fieldnew:
                    runningvec = [ "fieldreplace", "4", self.field, "2", self.fieldtarg, self.fieldnew ]
            case ModMode.MARKUP:
                if len(self.files) != 1:
                    return []
                if (len(self.markadd) < 1) or (len(self.markrem) < 1):
                    return []
                if (len(self.types) < 1):
                    return []
                runningvec.append(self.files[0])
                runningvec.extend(build_single("add", None, self.markadd))
                runningvec.extend(build_single("rem", None, self.markrem))
                runningvec.extend(build_single("type", None, self.files))
                runningvec.insert(0, str(len(runningvec)))
                runningvec.insert(0, "markupdate")
            case ModMode.TARGRM:
                runningvec = [ "targetremove", "2", self.field, self.fieldtarg ]
        return runningvec
