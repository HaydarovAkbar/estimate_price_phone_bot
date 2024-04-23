from telegram import Update
from telegram.ext import CallbackContext
from telegram import ParseMode

from .keyboards import KeyboardBase as kb
from .texts import Message as msg_txt

from db.models import User, Channels, Categories, Capacities, Products, Colors
from states import States as st


def start(update: Update, context: CallbackContext):
    user = User.objects.get_or_create(chat_id=update.effective_user.id, defaults={
        'fullname': update.effective_user.full_name,
        'username': update.effective_user.username,
        'language': 'uz',
        'is_active': True,
    })[0]
    channels = Channels.objects.filter(is_active=True)
    if channels.exists():
        i = int()
        locout_ch = list()
        for channel in channels:
            try:
                is_followers = context.bot.get_chat_member(channel.chat_id, user.chat_id)
            except Exception:
                for admin in User.objects.filter(is_admin=True):
                    context.bot.send_message(chat_id=admin.chat_id,
                                             text=msg_txt.not_admin.get(admin.language).format(channel.title))
                break
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
    if product.first().capacity.count() > 0:
        capacities = product.first().capacity
        update.message.reply_text(msg_txt.get_capacity[user.language].format(update.message.text),
                                  reply_markup=kb.reply_buttons(capacities.all(), main=True))
        return st.GET_CAPACITY
    else:
        colors = product.first().color.all()
        update.message.reply_text(msg_txt.get_color[user.language],
                                  reply_markup=kb.reply_buttons(colors, main=True))
        return st.GET_COLOR


def get_capacity_product(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_product[user.language].format(context.user_data['product'].title),
                                  reply_markup=kb.reply_buttons(Products.objects.all(), main=True))
        return st.GET_PRODUCT
    capacity = Capacities.objects.filter(title=update.message.text)
    if not capacity.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].capacity.all(), main=True))
        return st.GET_CAPACITY
    context.user_data['capacity'] = capacity.first()
    colors = context.user_data['product'].color.all()
    update.message.reply_text(msg_txt.get_color[user.language],
                              reply_markup=kb.reply_buttons(colors, main=True))
    return st.GET_COLOR


def get_color(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_capacity[user.language].format(context.user_data['product'].title),
                                  reply_markup=kb.reply_buttons(context.user_data['product'].capacity.all(), main=True))
        return st.GET_CAPACITY
    color = Colors.objects.filter(title=update.message.text)
    if not color.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].color.all(), main=True))
        return st.GET_COLOR
    context.user_data['color'] = color.first()
    memories = context.user_data['product'].memory.all()
    update.message.reply_text(msg_txt.get_memory[user.language],
                              reply_markup=kb.reply_buttons(memories, main=True))
    return st.GET_MEMORY


def get_memory(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_color[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].color.all(), main=True))
        return st.GET_COLOR
    memory = context.user_data['product'].memory.filter(title=update.message.text)
    if not memory.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].memory.all(), main=True))
        return st.GET_MEMORY
    context.user_data['memory'] = memory.first()
    documents = context.user_data['product'].document.all()
    update.message.reply_text(msg_txt.get_document[user.language],
                              reply_markup=kb.reply_buttons(documents, main=True))
    return st.GET_DOCUMENT


def get_document(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_memory[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].memory.all(), main=True))
        return st.GET_MEMORY
    document = context.user_data['product'].document.filter(title=update.message.text)
    if not document.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].document.all(), main=True))
        return st.GET_DOCUMENT
    context.user_data['document'] = document.first()
    countries = context.user_data['product'].country.all()
    update.message.reply_text(msg_txt.get_country[user.language],
                              reply_markup=kb.reply_buttons(countries, main=True))
    return st.GET_COUNTRY


def get_country(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_document[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].document.all(), main=True))
        return st.GET_DOCUMENT
    country = context.user_data['product'].country.filter(title=update.message.text)
    if not country.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].country.all(), main=True))
        return st.GET_COUNTRY
    context.user_data['country'] = country.first()
    statuses = context.user_data['product'].status.all()
    update.message.reply_text(msg_txt.get_status[user.language],
                              reply_markup=kb.reply_buttons(statuses, main=True))
    return st.GET_STATUS


def get_status(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    status = context.user_data['product'].status.filter(title=update.message.text)
    if not status.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].status.all(), main=True))
        return st.GET_STATUS

    # hashtags = context.user_data['product'].hashtags
    # fullname = user.fullname
    name = context.user_data['product'].title
    capacity = context.user_data.get('capacity', False)
    color = context.user_data['color'].title
    memory = context.user_data['memory'].title
    document = context.user_data['document'].title
    country = context.user_data['country'].title
    price = context.user_data['product'].price
    status = update.message.text
    # user_id = user.chat_id
    if capacity:
        msg_uz = f"""
<b>📲 Telefon:</b> {name}

<b>🛠 Shikast yetganmi: </b> {status}
<b>🔋 Batareyka:</b>  {capacity.title}
<b>▪️ Rangi:</b> {color}
<b>💾 Xotirasi:</b>  {memory}
<b>📦 Karobka Dok:</b>  {document}
<b>📬 Ishlab chiqarilgan joyi:</b>  {country}

<b>💰 Narxi:</b> {price}

<i>Bizni rasmiy telegram kanalimiz 👇</i>

<b><a href="https://t.me/PhoneSell_uz">TELEGRAM</a> | <a href="https://t.me/phonesell_admin">ADMIN</a></b>
"""
        msg_ru = f"""
<b>📲 Телефон:</b> {name}

<b>🛠 Сломан ли: </b> {status}
<b>🔋 Батарея:</b>  {capacity.title}
<b>▪️ Цвет:</b> {color}
<b>💾 Память:</b>  {memory}
<b>📦 Коробка Док:</b>  {document}
<b>📬 Страна производства:</b>  {country}

<b>💰 Цена:</b> {price}

<i>Подпишитесь на наш официальный телеграм канал 👇</i>  

<b><a href="https://t.me/PhoneSell_uz">TELEGRAM</a> | <a href="https://t.me/phonesell_admin">ADMIN</a></b>
"""
    else:
        msg_uz = f"""
<b>📲 Telefon:</b> {name}

<b>🛠 Shikast yetganmi: </b> {status}
<b>▪️ Rangi:</b> {color}
<b>💾 Xotirasi:</b>  {memory}
<b>📦 Karobka Dok:</b>  {document}
<b>📬 Ishlab chiqarilgan joyi:</b>  {country}

<b>💰 Narxi:</b> {price}

<i>Bizni rasmiy telegram kanalimiz 👇</i>

<b><a href="https://t.me/PhoneSell_uz">TELEGRAM</a> | <a href="https://t.me/phonesell_admin">ADMIN</a></b>
        """
        msg_ru = f"""
<b>📲 Телефон:</b> {name}

<b>🛠 Сломан ли: </b> {status}
<b>▪️ Цвет:</b> {color}
<b>💾 Память:</b>  {memory}
<b>📦 Коробка Док:</b>  {document}
<b>📬 Страна производства:</b>  {country}

<b>💰 Цена:</b> {price}

<i>Подпишитесь на наш официальный телеграм канал 👇</i>

<b><a href="https://t.me/PhoneSell_uz">TELEGRAM</a> | <a href="https://t.me/phonesell_admin">ADMIN</a></b>
        """
    msg = msg_ru if user.language == 'ru' else msg_uz
    update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    update.message.reply_html(msg_txt.help_txt[user.language], reply_markup=kb.sell_product(user.language))
    return st.SEND_CHANNEL


def send_admin(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.get_status[user.language],
                                  reply_markup=kb.reply_buttons(context.user_data['product'].status.all(), main=True))
        return st.GET_STATUS
    # admins = User.objects.filter(is_admin=True)
    # for admin in admins:
    #     context.bot.send_message(chat_id=admin.chat_id, text=update.message.text)
    update.message.reply_html(msg_txt.price_txt[user.language], reply_markup=kb.admin_inline('https://t.me/phonesell_admin'))
    return st.SEND_CHANNEL


def change_language(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    update.message.reply_text(msg_txt.choose_language.get(user.language),
                              reply_markup=kb.languages())
    return st.CHOOSE_LANGUAGE


def choose_language(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.main.get(user.language).format(user.fullname),
                                  reply_markup=kb.get_main_menu(user.language))
        return st.MAIN_MENU
    if update.message.text == '🇺🇿 O`zbekcha':
        user.language = 'uz'
    else:
        user.language = 'ru'
    user.save()
    update.message.reply_html(msg_txt.success_lang_change.get(user.language),
                              reply_markup=kb.get_main_menu(user.language))
    return st.MAIN_MENU


def report_admin(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    update.message.reply_html(msg_txt.report_admin[user.language],
                              reply_markup=kb.back(user.language))
    return st.REPORT_ADMIN


def get_report(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == msg_txt.back.get(user.language):
        update.message.reply_text(msg_txt.report_admin[user.language],
                                  reply_markup=kb.get_report_menu(user.language))
        return st.REPORT_ADMIN
    try:
        update.message.forward(5911729079)
    except Exception:
        admins = User.objects.filter(is_admin=True)
        for admin in admins:
            update.message.forward(admin.chat_id)
    update.message.reply_text(msg_txt.success[user.language], reply_markup=kb.get_main_menu(user.language))
    return st.MAIN_MENU
