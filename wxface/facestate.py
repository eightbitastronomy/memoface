from enum import Enum


class FaceState(Enum):
    FNDFILE = 1
    FNDMARK = 2
    FNDTYPE = 3
    MNGADDREC = 4
    MNGMODREC = 5
    MNGREMREC = 6
    MNGIMPORT = 7
    MNGEXPORT = 8