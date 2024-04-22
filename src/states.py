from enum import Enum, auto


class States(Enum):
    START = auto()
    FOLLOWERS = auto()
    MAIN_MENU = auto()

    ADMIN = auto()
    ADD_ADMIN = auto()
    ADMINS = auto()
    ADD_DATA = auto()
    SALE_PRODUCT = auto()
    GET_CAPACITY = auto()
    GET_PRODUCT = auto()
    GET_COLOR = auto()
    GET_MEMORY = auto()
    GET_DOCUMENT = auto()
    GET_COUNTRY = auto()
    GET_STATUS = auto()

    SEND_CHANNEL = auto()