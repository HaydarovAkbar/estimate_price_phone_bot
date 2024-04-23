from .texts import KeyboardsTexts as msg_txt
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class KeyboardBase:
    def __init__(self, *args, **kwargs):
        self._buttons = []
        self._keyboard = []

    def add(self, *args):
        self._buttons.extend(args)

    def row(self, *args):
        self._keyboard.append(args)

    def render(self):
        return self._keyboard

    def __str__(self):
        return str(self._keyboard)

    def __repr__(self):
        return str(self._keyboard)

    @staticmethod
    def channels(channels):
        keyboard = []
        for channel in channels:
            keyboard.append(
                [InlineKeyboardButton(channel.title, url=channel.url)]
            )
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_main_menu(lang='uz'):
        txt = msg_txt.main.get(lang)
        kb = ReplyKeyboardMarkup(
            [
                [KeyboardButton(txt[0]), KeyboardButton(txt[1])],
                [KeyboardButton(txt[2])],
            ],
            resize_keyboard=True
        )
        return kb

    @staticmethod
    def get_report_menu(lang='uz'):
        txt = msg_txt.report.get(lang)
        kb = ReplyKeyboardMarkup(
            [
                [KeyboardButton(txt[0]), KeyboardButton(txt[1])],
                [KeyboardButton(txt[2])],
            ],
            resize_keyboard=True
        )
        return kb

    @staticmethod
    def back(lang='uz'):
        txt = msg_txt.back.get(lang)
        kb = ReplyKeyboardMarkup(
            [
                [KeyboardButton(txt)],
            ],
            resize_keyboard=True
        )
        return kb

    @staticmethod
    def fuel_types(fuel_types):
        keyboard = []
        for fuel_type in fuel_types:
            keyboard.append(
                [InlineKeyboardButton(fuel_type.fuel_type.title, callback_data=f'{fuel_type.fuel_type.id}')])
        keyboard.append([InlineKeyboardButton(msg_txt.back.get('uz'), callback_data='back')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def reply_buttons(buttons, main=False):
        keyboard, row = [], []
        for button in buttons:
            row.append(KeyboardButton(button.title))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        if main:
            keyboard.append([KeyboardButton(msg_txt.back.get('uz')), KeyboardButton(msg_txt.back_main.get('uz'))])
        else:
            keyboard.append([KeyboardButton(msg_txt.back.get('uz'))])
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def languages():
        keyboard, row = [], []
        for lang in msg_txt.languages:
            row.append(KeyboardButton(lang))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
