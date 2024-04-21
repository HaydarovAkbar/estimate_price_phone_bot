from telegram import Update
from telegram.ext import CallbackContext

from .texts import Message as msg_txt
from .keyboards import KeyboardBase as kb

from db.models import User, Channels, Categories, Capacities

from states import States as st


def start(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    channels = Channels.objects.filter(is_active=True)
    if channels.exists():
        i = int()
        locout_ch = list()
        for channel in channels:
            is_followers = context.bot.get_chat_member(channel.chat_id, user.chat_id)
            if is_followers.status in ['member', 'administrator']:
                i += 1
            else:
                locout_ch.append(channel)
        if i == channels.count():
            update.message.reply_text(msg_txt.main.get(user.language).format(user.fullname),
                                      reply_markup=kb.get_main_menu(user.language))
            return st.MAIN_MENU
        else:
            update.message.reply_text(msg_txt.forced_labor.get(user.language),
                                      reply_markup=kb.channels(locout_ch))
            return st.FOLLOWERS
    else:
        update.message.reply_text(msg_txt.main.get(user.language).format(user.fullname),
                                  reply_markup=kb.get_main_menu(user.language))
        return st.MAIN_MENU


def followers(update: Update, context: CallbackContext):
    query = update.callback_query
    user = User.objects.get(chat_id=query.from_user.id)
    if query.data == 'confirm':
        query.delete_message()
        channels = Channels.objects.filter(is_active=True)
        i, locout_ch = int(), list()
        for channel in channels:
            is_followers = context.bot.get_chat_member(channel.chat_id, user.chat_id)
            if is_followers.status in ['member', 'administrator']:
                i += 1
            else:
                locout_ch.append(channel)
        if i == channels.count():
            context.bot.send_message(chat_id=user.chat_id, text=msg_txt.main.get(user.language).format(user.fullname),
                                     reply_markup=kb.get_main_menu(user.language))
            return st.MAIN_MENU
        else:
            context.bot.send_message(chat_id=user.chat_id, text=msg_txt.forced_labor.get(user.language),
                                     reply_markup=kb.channels(locout_ch))
            return st.FOLLOWERS
    else:
        query.delete_message()
        context.bot.send_message(chat_id=user.chat_id, text=msg_txt.main.get(user.language).format(user.fullname),
                                 reply_markup=kb.get_main_menu(user.language))
        return st.MAIN_MENU


def sale_product(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    categories = Categories.objects.filter(is_active=True)
    update.message.reply_text(msg_txt.sale_product[user.language], reply_markup=kb.reply_buttons(categories))
    return st.SALE_PRODUCT
