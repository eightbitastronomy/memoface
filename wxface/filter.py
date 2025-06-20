from wxface.commutility import build_single


class Filter:
    
    def __init__(self):
        self.marks = []
        self.files = []
        self.types = []
        self.equality = ""
        self.grepoption = "false"
        self.grepcase = "false"
        self.greplink = "false"
        self.mark_logic = "or"
        self.file_logic = "or"
        self.type_logic = "or"
    
    def add_marks(self, markvec):
        self.marks.extend(markvec)
        return self
        
    def add_files(self, filevec):
        self.files.extend(filevec)
        return self
        
    def add_types(self, typevec):
        self.types.extend(typevec)
        return self
        
    def set_grep_option(self, switch):
        self.grepoption = switch.lower()
        return self
    
    def set_grep_case(self, switch):
        self.grepcase = switch.lower()
        return self
    
    def set_grep_link(self, switch):
        self.greplink = switch.lower()
        return self
        
    def set_logic(self, ftype, flogic):
        if ftype == "mark":
            self.mark_logic = flogic.lower()
        elif ftype == "type":
            self.type_logic = flogic.lower()
        elif ftype == "file":
            self.file_logic = flogic.lower()
        return self
    
    def set_equality(self, feq):
        if feq in ("mark","file","type"):
            self.equality = feq
        return self        
    
#    def __form_filt(self, ftype, flogic, terms):
#        if (ftype == "") or (flogic == "") or (len(terms) < 1):
#            return []
#        returnbuf = [ftype, flogic, str(len(terms))] + terms
#        return returnbuf
    
    def form(self):
        #search # grep1 grep2 grep3 eq ...
        runningvec = []
        if len(self.marks) > 0:
            if self.equality == "mark":
                return []
            #runningvec += self.__form_filt("mark", self.mark_logic, self.marks)
            runningvec += build_single("mark", self.mark_logic, self.marks)
        if len(self.types) > 0:
            if self.equality == "type":
                return []
            #runningvec += self.__form_filt("type", self.type_logic, self.types)
            runningvec += build_single("type", self.type_logic, self.types)
        if len(self.files) > 0:
            if self.equality == "file":
                return []
            #runningvec += self.__form_filt("file", self.file_logic, self.files)
            runningvec += build_single("file", self.file_logic, self.files)
        runningvec.insert(0, str(len(runningvec)))
        runningvec = [self.grepoption, self.grepcase, self.greplink, self.equality] + runningvec
        #runningvec = ["search", str(len(runningvec))] + runningvec
        return runningvec
