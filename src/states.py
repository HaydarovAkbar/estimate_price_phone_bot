from enum import Enum, auto


class States(Enum):
    START = auto()
    FOLLOWERS = auto()
    MAIN_MENU = auto()

    ADMIN = auto()
    ADD_ADMIN = auto()
    ADMINS = auto()
    ADD_CHANNEL = auto()
    ADD_CHANNEL_URL = auto()
    ADD_CHANNEL_ID = auto()
    DELETE_CHANNEL = auto()

    REKLAMA = auto()

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
    CHOOSE_LANGUAGE = auto()
    REPORT_ADMIN = auto()