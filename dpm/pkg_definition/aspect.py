from enum import Enum


class Aspect(Enum):
    CONTAINS_BINARIES = 1
    VIRTUAL = 2
    CONTAINS_PKG_CONFIG = 4
