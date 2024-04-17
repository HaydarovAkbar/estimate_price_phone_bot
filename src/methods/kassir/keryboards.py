from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from .texts import KeyboardsTexts as txt


class KassirKeyboards:
    @staticmethod
    def back(lang='uz'):
        text = txt.back[lang]
        keyboard = [
            [KeyboardButton(text)],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def start(lang='uz'):
        text = txt.start[lang]
        keyboard = [
            [KeyboardButton(text)],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def fuel_types(fuel_types, lang='uz'):
        keyboard = []
        for fuel_type in fuel_types:
            keyboard.append([InlineKeyboardButton(fuel_type.title, callback_data=f'{fuel_type.id}')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def organ_fuel_types(organ_fuel_types, lang='uz'):
        keyboard = []
        for org_fuel_types in organ_fuel_types:
            keyboard.append(
                [InlineKeyboardButton(org_fuel_types.fuel_type.title, callback_data=f'{org_fuel_types.fuel_type.id}')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def organ_fuel_columns(organ_fuel_columns, lang='uz'):
        keyboard = []
        for organ_fuel_col in organ_fuel_columns:
            keyboard.append(
                [InlineKeyboardButton(organ_fuel_col.fuel_column.title,
                                      callback_data=f'{organ_fuel_col.fuel_column.id}')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def fuel_columns(columns, lang='uz'):
        keyboard = []
        for column in columns:
            keyboard.append([InlineKeyboardButton(column.title, callback_data=f'{column.id}')])
        keyboard.append([InlineKeyboardButton(txt.back[lang], callback_data='back')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_menu(lang='uz'):
        text = txt.back_to_menu[lang]
        keyboard = [
            [KeyboardButton(text)]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def data_types(lang='uz'):
        text = txt.data_types[lang]
        keyboard = [
            [text[0]],
            [text[1]],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def back_types(lang='uz'):
        text = txt.back_types[lang]
        keyboard = [
            [text[0], text[1]],
            [text[2]]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def back_types2(lang='uz'):
        text = txt.back_types2[lang]
        keyboard = [
            [text[0], text[1]],
            [text[2]]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
