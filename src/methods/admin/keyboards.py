from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from ..dictionary import AdminButton as bt


class AdminKeyboards:
    @staticmethod
    def base():
        msg = bt.base
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0], msg[1]],
                [msg[2], msg[3]],
                [msg[4]],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def back():
        msg = bt.back
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0]],
            ],
            resize_keyboard=True
        )
        return keyboard

    @staticmethod
    def message():
        msg = bt.message
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [msg[0]],
                [msg[1]],
                [msg[2]],
                [msg[3]],
            ],
            resize_keyboard=True
        )
        return keyboard


class KeyboardsAdmin:
    # ...
    @staticmethod
    def get_users(user_list):
        keyboard = []
        for user in user_list:
            keyboard.append([InlineKeyboardButton(user.get_fullname(), callback_data=f'{user.id}')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_admin_menu(lang='uz'):
        bt_txt = bt.adm_menu[lang]
        keyboard = [
            [KeyboardButton(bt_txt[0]), KeyboardButton(bt_txt[4])],
            [KeyboardButton(bt_txt[1]), KeyboardButton(bt_txt[2])],
            [KeyboardButton(bt_txt[3])],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def get_user_menu(lang='uz'):
        bt_txt = bt.adm_user_menu[lang]
        keyboard = [
            [KeyboardButton(bt_txt[0]), KeyboardButton(bt_txt[1])],
            [KeyboardButton(bt_txt[2])],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def adm_settings(lang='uz'):
        bt_txt = bt.adm_settings[lang]
        keyboard = [
            [KeyboardButton(bt_txt[0])],
            [KeyboardButton(bt_txt[1])],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def get_lang():
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton('🇺🇿 O\'zbekcha', callback_data='uz')],
            [InlineKeyboardButton('🇷🇺 Русский', callback_data='ru')],
            [InlineKeyboardButton('🇬🇧 English', callback_data='en')],
        ])
        return keyboard

    @staticmethod
    def back(lang='uz'):
        bt_txt = bt.adm_settings[lang]
        keyboard = [
            [KeyboardButton(bt_txt[1])],
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def roles(user_role='', lang='uz'):
        bt_txt = bt.adm_roles[lang]
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(bt_txt[0] + (' - ✅' if user_role == 'leader' else ''), callback_data='leader')],
            [InlineKeyboardButton(bt_txt[1] + (' - ✅' if user_role == 'cashier' else ''), callback_data='cashier')],
            [InlineKeyboardButton(bt_txt[2] + (' - ✅' if user_role == 'leader_cashier' else ''),
                                  callback_data='leader_cashier')],
            [InlineKeyboardButton(bt_txt[4], callback_data='delete'),
             InlineKeyboardButton(bt_txt[3], callback_data='back')],
        ])
        return keyboard

    @staticmethod
    def user_list(users, lang='uz'):
        keyboard, txt = [], bt.inline_back[lang]
        for user in users:
            keyboard.append([InlineKeyboardButton(user.get_user(), callback_data=f'{user.chat_id}')])
        keyboard.append([InlineKeyboardButton(txt, callback_data='back')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def user_change(user_roles, lang='uz'):
        bt_txt = bt.adm_roles[lang]
        if "ADMIN" in user_roles and "KASSIR" in user_roles:
            keyboard = [
                [KeyboardButton(bt_txt[4]), KeyboardButton(bt_txt[0])],
                [KeyboardButton(bt_txt[2] + "- ✅"), KeyboardButton(bt_txt[1])],
                [KeyboardButton(bt_txt[3])],
            ]
        elif "KASSIR" in user_roles:
            keyboard = [
                [KeyboardButton(bt_txt[4]), KeyboardButton(bt_txt[0])],
                [KeyboardButton(bt_txt[2]), KeyboardButton(bt_txt[1] + "- ✅")],
                [KeyboardButton(bt_txt[3])],
            ]
        elif "ADMIN" in user_roles:
            keyboard = [
                [KeyboardButton(bt_txt[4]), KeyboardButton(bt_txt[0] + "- ✅")],
                [KeyboardButton(bt_txt[2]), KeyboardButton(bt_txt[1])],
                [KeyboardButton(bt_txt[3])],
            ]
        else:
            keyboard = [
                [KeyboardButton(bt_txt[4]), KeyboardButton(bt_txt[0])],
                [KeyboardButton(bt_txt[2]), KeyboardButton(bt_txt[1])],
                [KeyboardButton(bt_txt[3])],
            ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    @staticmethod
    def organization_list(org_list, lang='uz'):
        keyboard, txt = [], bt.inline_back[lang]
        for org in org_list:
            keyboard.append([InlineKeyboardButton(org.title, callback_data=f'{org.id}')])
        keyboard.append([InlineKeyboardButton(txt, callback_data='back')])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def organ_fuel_column(fuel_types, selected):
        keyboard = []
        for fuel in fuel_types:
            if str(fuel.id) in selected:
                keyboard.append([InlineKeyboardButton(f'{fuel.title} - ✅', callback_data=f'{fuel.id}')])
            else:
                keyboard.append([InlineKeyboardButton(fuel.title, callback_data=f'{fuel.id}')])
        keyboard.append([InlineKeyboardButton('✅ Tasdiqlash ✅', callback_data='confirm')])
        return InlineKeyboardMarkup(keyboard)
