from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from .message import KeyboardsAdmin as bt


class AdminKeyboards:
    @staticmethod
    def base(user_lang='uz'):
        msg = bt.base.get(user_lang)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0], msg[1]],
                [msg[2], msg[3]],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def back(user_lang='uz'):
        msg = bt.back.get(user_lang)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0]],
            ],
            resize_keyboard=True
        )
        return keyboard
