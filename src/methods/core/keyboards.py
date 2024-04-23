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
                [KeyboardButton(txt[0])],
                [KeyboardButton(txt[1]), KeyboardButton(txt[2])],
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
    def reply_buttons(buttons, main=False, lang='uz'):
        keyboard, row = [], []
        for button in buttons:
            row.append(KeyboardButton(button.title))
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        if main:
            keyboard.append([KeyboardButton(msg_txt.back.get(lang)), KeyboardButton(msg_txt.back_main.get(lang))])
        else:
            keyboard.append([KeyboardButton(msg_txt.back.get(lang))])
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

    @staticmethod
    def sell_product(lang='uz'):
        msg = msg_txt.sale_product.get(lang)
        keyboard = [
            [KeyboardButton(msg[0]), KeyboardButton(msg[1])],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def admin_inline(admin_url):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('📤 Chekni yuborish', url=admin_url)]
        ])
