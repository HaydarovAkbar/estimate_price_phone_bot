from telegram import Update
from telegram.ext import CallbackContext

from .texts import Message as msg_txt
from .keyboards import KeyboardBase as kb

from db.models import User, Channels, Categories, Capacities, Products, Colors

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
    categories = Categories.objects.all()
    update.message.reply_text(msg_txt.sale_product[user.language], reply_markup=kb.reply_buttons(categories))
    return st.SALE_PRODUCT


def get_category(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.main.get(user.language).format(user.fullname),
                                  reply_markup=kb.get_main_menu(user.language))
        return st.MAIN_MENU
    category = Categories.objects.filter(title=update.message.text)
    if not category.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(Categories.objects.all()))
        return st.SALE_PRODUCT
    products = Products.objects.filter(category=category.first())
    update.message.reply_text(msg_txt.get_product[user.language].format(update.message.text),
                              reply_markup=kb.reply_buttons(products))
    return st.GET_PRODUCT


def get_capacity(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.sale_product[user.language],
                                  reply_markup=kb.reply_buttons(Categories.objects.all()))
        return st.SALE_PRODUCT
    product = Products.objects.filter(title=update.message.text)
    if not product.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(Products.objects.all()))
        return st.GET_PRODUCT
    context.user_data['product'] = product.first()
    print(product.first().capacity.count())
    if product.first().capacity.count() > 0:
        capacities = product.first().capacity
        update.message.reply_text(msg_txt.get_capacity[user.language].format(update.message.text),
                                  reply_markup=kb.reply_buttons(capacities.all()))
        return st.GET_CAPACITY
    else:
        colors = product.first().color.all()
        update.message.reply_text(msg_txt.get_color[user.language],
                                  reply_markup=kb.reply_buttons(colors))
        return st.GET_COLOR


def get_capacity_product(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_product[user.language].format(context.user_data['product'].title),
                                  reply_markup=kb.reply_buttons(Products.objects.all()))
        return st.GET_PRODUCT
    capacity = Capacities.objects.filter(title=update.message.text)
    print(capacity.all())
    if not capacity.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].capacity.all()))
        return st.GET_CAPACITY
    context.user_data['capacity'] = capacity.first()
    colors = context.user_data['product'].color.all()
    update.message.reply_text(msg_txt.get_color[user.language],
                              reply_markup=kb.reply_buttons(colors))
    return st.GET_COLOR



def get_color(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_capacity[user.language].format(context.user_data['product'].title),
                                  reply_markup=kb.reply_buttons(context.user_data['product'].capacity.all()))
        return st.GET_CAPACITY
    color = Colors.objects.filter(title=update.message.text)
    if not color.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].color.all()))
        return st.GET_COLOR
    context.user_data['color'] = color.first()
    memories = context.user_data['product'].memory.all()
    update.message.reply_text(msg_txt.get_memory[user.language],
                              reply_markup=kb.reply_buttons(memories))
    return st.GET_MEMORY


def get_memory(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_color[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].color.all()))
        return st.GET_COLOR
    memory = context.user_data['product'].memory.filter(title=update.message.text)
    if not memory.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].memory.all()))
        return st.GET_MEMORY
    context.user_data['memory'] = memory.first()
    documents = context.user_data['product'].document.all()
    update.message.reply_text(msg_txt.get_document[user.language],
                              reply_markup=kb.reply_buttons(documents))
    return st.GET_DOCUMENT


def get_document(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_memory[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].memory.all()))
        return st.GET_MEMORY
    document = context.user_data['product'].document.filter(title=update.message.text)
    if not document.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].document.all()))
        return st.GET_DOCUMENT
    update.message.reply_text(msg_txt.success[user.language])
    return st.MAIN_MENU