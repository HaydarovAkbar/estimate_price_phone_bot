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
                [msg[4], msg[5]],
                [msg[6]],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def back(user_lang='uz'):
        msg = bt.back.get(user_lang)
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def channels(channels):
        keyboard = []
        for channel in channels:
            keyboard.append(
                [InlineKeyboardButton(channel.title, url=channel.url)]
            )
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def users(users):
        keyboard = []
        for user in users:
            keyboard.append(
                [InlineKeyboardButton(user.get_fullname(), callback_data=f'{user.chat_id}')]
            )
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def all_channels(channels):
        keyboard = []
        for channel in channels:
            keyboard.append(
                [InlineKeyboardButton(channel.title, callback_data=f'{channel.chat_id}')]
            )
        return InlineKeyboardMarkup(keyboard)