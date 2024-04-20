from enum import Enum, auto


class States(Enum):
    START = auto()
    FOLLOWERS = auto()
    MAIN_MENU = auto()

    ADMIN = auto()
    ADD_ADMIN = auto()
