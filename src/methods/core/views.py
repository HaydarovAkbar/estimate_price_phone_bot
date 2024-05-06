from telegram import Update
from telegram.ext import CallbackContext
from telegram import ParseMode

from .keyboards import KeyboardBase as kb
from .texts import Message as msg_txt

from db.models import User, Channels, Categories, Capacities, Products, Colors, ProductCriteria, Memories, Documents, \
    Countries, Statuses
from states import States as st


def check_user(update: Update, context: CallbackContext):
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
                return st.FOLLOWERS
            if is_followers.status in ['member', 'administrator', 'owner', 'creator']:
                i += 1
            else:
                locout_ch.append(channel)
        if i != channels.count():
            update.message.reply_text(msg_txt.forced_labor.get(user.language),
                                      reply_markup=kb.channels(locout_ch, user.language))
            return st.FOLLOWERS
    return True


def start(update: Update, context: CallbackContext):
    # print("Kutish buvoti")
    user = User.objects.get_or_create(chat_id=update.effective_user.id, defaults={
        'fullname': update.effective_user.full_name,
        'username': update.effective_user.username,
        'language': 'uz',
        'is_active': True,
    })[0]
    # print("User:", user)
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
                return st.FOLLOWERS
            if is_followers.status in ['member', 'administrator', 'owner', 'creator']:
                i += 1
            else:
                locout_ch.append(channel)
        if i == channels.count():
            update.message.reply_text(msg_txt.main.get(user.language).format(user.fullname),
                                      reply_markup=kb.get_main_menu(user.language))
            return st.MAIN_MENU
        else:
            update.message.reply_text(msg_txt.forced_labor.get(user.language),
                                      reply_markup=kb.channels(locout_ch, user.language))
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
                                     reply_markup=kb.channels(locout_ch, user.language))
            return st.FOLLOWERS
    else:
        query.delete_message()
        context.bot.send_message(chat_id=user.chat_id, text=msg_txt.main.get(user.language).format(user.fullname),
                                 reply_markup=kb.get_main_menu(user.language))
        return st.MAIN_MENU


def sale_product(update: Update, context: CallbackContext):
    check_user(update, context)
    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    categories = Categories.objects.all()
    update.message.reply_text(msg_txt.sale_product[user.language],
                              reply_markup=kb.reply_buttons(categories, lang=user_lang))
    return st.SALE_PRODUCT


def get_category(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    check_user(update, context)
    category = Categories.objects.filter(title=update.message.text)
    if not category.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(Categories.objects.all(), lang=user_lang))
        return st.SALE_PRODUCT
    products = Products.objects.filter(category=category.first())
    update.message.reply_text(msg_txt.get_product[user.language].format(update.message.text),
                              reply_markup=kb.reply_buttons(products, lang=user_lang))
    return st.GET_PRODUCT


def get_capacity(update: Update, context: CallbackContext):
    check_user(update, context)
    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    product = Products.objects.filter(title=update.message.text)
    if not product.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(Products.objects.all(), lang=user_lang))
        return st.GET_PRODUCT
    context.user_data['product'] = product.first()
    product_capacity = ProductCriteria.objects.filter(product=product.first()).filter(capacity__isnull=False)
    if product_capacity.count() > 0:
        capacities = product_capacity.filter(capacity__isnull=False).values('capacity').distinct()
        model_capacity = Capacities.objects.filter(id__in=capacities)
        update.message.reply_text(msg_txt.get_capacity[user.language].format(update.message.text),
                                  reply_markup=kb.reply_buttons(model_capacity, main=True, lang=user_lang))
        return st.GET_CAPACITY
    else:
        colors = ProductCriteria.objects.filter(product=product.first()).filter(color__isnull=False).values(
            'color').distinct()
        colors = Colors.objects.filter(id__in=colors)
        update.message.reply_text(msg_txt.get_color[user.language],
                                  reply_markup=kb.reply_buttons(colors, main=True, lang=user_lang))
        return st.GET_COLOR


def get_capacity_product(update: Update, context: CallbackContext):
    check_user(update, context)
    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    product = context.user_data['product']
    product_capacity = ProductCriteria.objects.filter(product=product).filter(capacity__isnull=False)
    if product_capacity.count() == 0:
        colors = ProductCriteria.objects.filter(product=product).filter(color__isnull=False).values(
            'color').distinct()
        colors = Colors.objects.filter(id__in=colors)
        update.message.reply_text(msg_txt.get_color[user.language],
                                  reply_markup=kb.reply_buttons(colors, main=True, lang=user_lang))
        return st.GET_COLOR
    capacity = Capacities.objects.filter(title=update.message.text)
    if not capacity.exists():
        capacities = product_capacity.filter(capacity__isnull=False).values('capacity').distinct()
        model_capacity = Capacities.objects.filter(id__in=capacities)
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(model_capacity, main=True,
                                                                lang=user_lang))
        return st.GET_CAPACITY
    context.user_data['capacity'] = capacity.first()
    colors = ProductCriteria.objects.filter(product=product).filter(color__isnull=False).values(
        'color').distinct()
    colors = Colors.objects.filter(id__in=colors)
    update.message.reply_text(msg_txt.get_color[user.language],
                              reply_markup=kb.reply_buttons(colors, main=True, lang=user_lang))
    return st.GET_COLOR


def get_color(update: Update, context: CallbackContext):
    check_user(update, context)
    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    color = Colors.objects.filter(title=update.message.text)
    product = context.user_data['product']
    if not color.exists():
        colors = ProductCriteria.objects.filter(product=product).filter(color__isnull=False).values(
            'color').distinct()
        colors = Colors.objects.filter(id__in=colors)
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(colors, main=True,
                                                                lang=user_lang))
        return st.GET_COLOR
    context.user_data['color'] = color.first()
    memories = ProductCriteria.objects.filter(product=product).filter(memory__isnull=False).values(
        'memory').distinct()
    memories = Memories.objects.filter(id__in=memories)
    update.message.reply_text(msg_txt.get_memory[user.language],
                              reply_markup=kb.reply_buttons(memories, main=True, lang=user_lang))
    return st.GET_MEMORY


def get_memory(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    product = context.user_data['product']
    memory = Memories.objects.filter(title=update.message.text)
    if not memory.exists():
        memories = Memories.objects.filter(product=product).filter(memory__isnull=False).values(
            'memory').distinct()
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(memories, main=True,
                                                                lang=user_lang))
        return st.GET_MEMORY
    context.user_data['memory'] = memory.first()
    documents = ProductCriteria.objects.filter(product=product).filter(document__isnull=False).values(
        'document').distinct()
    documents = Documents.objects.filter(id__in=documents)
    update.message.reply_text(msg_txt.get_document[user.language],
                              reply_markup=kb.reply_buttons(documents, main=True, lang=user_lang))
    return st.GET_DOCUMENT


def get_document(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    product = context.user_data['product']
    document = Documents.objects.filter(title=update.message.text)
    if not document.exists():
        documents = Documents.objects.filter(product=product).filter(document__isnull=False).values(
            'document').distinct()
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(documents, True,
                                                                user_lang))
        return st.GET_DOCUMENT
    context.user_data['document'] = document.first()
    countries = ProductCriteria.objects.filter(product=product).filter(country__isnull=False).values(
        'country').distinct()
    countries = Countries.objects.filter(id__in=countries)
    update.message.reply_text(msg_txt.get_country[user.language],
                              reply_markup=kb.reply_buttons(countries, True, user_lang))
    return st.GET_COUNTRY


def get_country(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language
    product = context.user_data['product']
    country = Countries.objects.filter(title=update.message.text)
    if not country.exists():
        countries = Countries.objects.filter(product=product).filter(country__isnull=False).values(
            'country').distinct()
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(countries, main=True,
                                                                lang=user_lang))
        return st.GET_COUNTRY
    context.user_data['country'] = country.first()
    statuses = ProductCriteria.objects.filter(product=product).filter(status__isnull=False).values(
        'status').distinct()
    statuses = Statuses.objects.filter(id__in=statuses)
    update.message.reply_text(msg_txt.get_status[user.language],
                              reply_markup=kb.reply_buttons(statuses, main=True, lang=user_lang))
    return st.GET_STATUS


def get_status(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    status = Statuses.objects.filter(title=update.message.text)
    product = context.user_data['product']
    user_lang = user.language
    if not status.exists():
        statuses = Statuses.objects.filter(product=product).filter(status__isnull=False).values(
            'status').distinct()
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(statuses, main=True,
                                                                lang=user_lang))
        return st.GET_STATUS
    filters = dict()
    filters['product'] = product
    filters['status'] = status.first()
    filters['capacity'] = context.user_data.get('capacity', None)
    filters['color'] = context.user_data['color']
    filters['memory'] = context.user_data['memory']
    filters['document'] = context.user_data['document']
    filters['country'] = context.user_data['country']
    product_criteria = ProductCriteria.objects.filter(**filters)
    if not product_criteria.exists():
        update.message.reply_text(msg_txt.not_found[user.language],
                                  reply_markup=kb.reply_buttons(Statuses.objects.all(), main=True, lang=user_lang))
        return st.GET_STATUS
    price = product_criteria.first().price
    name = context.user_data['product'].title
    capacity = context.user_data.get('capacity', False)
    color = context.user_data['color'].title
    memory = context.user_data['memory'].title
    document = context.user_data['document'].title
    country = context.user_data['country'].title
    status = update.message.text
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
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    update.message.reply_html(msg_txt.price_txt[user.language],
                              reply_markup=kb.admin_inline('https://t.me/phonesell_admin'))
    return st.SEND_CHANNEL


def change_language(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    update.message.reply_text(msg_txt.choose_language.get(user.language),
                              reply_markup=kb.languages())
    return st.CHOOSE_LANGUAGE


def choose_language(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    if update.message.text == '🇺🇿 O`zbekcha':
        user.language = 'uz'
    else:
        user.language = 'ru'
    user.save()
    update.message.reply_html(msg_txt.success_lang_change.get(user.language),
                              reply_markup=kb.get_main_menu(user.language))
    return st.MAIN_MENU


def report_admin(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    update.message.reply_html(msg_txt.report_admin[user.language],
                              reply_markup=kb.back(user.language))
    return st.REPORT_ADMIN


def get_report(update: Update, context: CallbackContext):
    check_user(update, context)

    user = User.objects.get(chat_id=update.effective_user.id)
    try:
        update.message.forward(5911729079)
    except Exception:
        admins = User.objects.filter(is_admin=True)
        for admin in admins:
            update.message.forward(admin.chat_id)
    update.message.reply_text(msg_txt.success[user.language], reply_markup=kb.get_main_menu(user.language))
    return st.MAIN_MENU
