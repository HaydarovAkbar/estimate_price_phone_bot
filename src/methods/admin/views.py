from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
import openpyxl

from .keyboards import AdminKeyboards as K
from .message import MessageText as T

from states import States as S
from db.models import User, Channels, Categories, Capacities, Products, Documents, Countries, Statuses, Memories, Colors


def admin(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_text(T().main[user_lang].format(tg_user.full_name),
                              reply_markup=K().base(user_lang))
    return S.ADMIN


def add_admin(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_text(T().add_admin[user_lang],
                              reply_markup=K().back(user_lang))
    return S.ADD_ADMIN


def get_admin_id(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    try:
        user_id = int(update.message.text)
    except ValueError:
        update.message.reply_text(T().error_id[user_lang])
        return S.ADD_ADMIN
    user, _ = User.objects.get_or_create(chat_id=user_id,
                                         defaults={'chat_id': user_id, 'language': user_lang, 'is_active': True,
                                                   'is_admin': True})
    if _ or not user.is_admin:
        if not user.is_active:
            user.is_active = True
            user.save()
        update.message.reply_text(T().success[user_lang], reply_markup=K().base(user_lang))
    else:
        update.message.reply_text(T().already_admin[user_lang],
                                  reply_markup=K().base(user_lang))
    return S.ADMIN


def get_admins(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    admins = User.objects.filter(is_active=True, is_admin=True)
    if admins.exists():
        text = T().admins[user_lang]
        i = 1
        for admin in admins:
            text += f"{i}) {admin.get_fullname()}\n"
            i += 1
        text += T().delete_admin[user_lang]
        update.message.reply_text(text, reply_markup=K().users(admins))
        return S.ADMINS
    else:
        update.message.reply_text(T().no_admins[user_lang], reply_markup=K().base(user_lang))
    return S.ADMIN


def delete_admin(update: Update, context: CallbackContext):
    tg_user = update.callback_query.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    user_id = int(update.callback_query.data)
    user = User.objects.get(chat_id=user_id)
    user.is_admin = False
    user.save()
    update.callback_query.delete_message()
    update.callback_query.bot.send_message(chat_id=tg_user.id, text=T().success[user_lang])
    return S.ADMIN


def get_users(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    all_text = "{:<1} {:<8} {:<23}\n\n".format("ID ||", "   Name      ||", "   Date")
    users = User.objects.filter(is_active=True).order_by('-created_at')[0:50]
    i = 1
    for user in users:
        all_text += "{:<1} | {:<8} | {:<23}\n".format(i, user.fullname,
                                                      user.created_at.strftime('%Y-%m-%d %H:%M'))
        i += 1
    update.message.reply_text(all_text, reply_markup=K().base(user_lang))
    return S.ADMIN


def add_data(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_text(T().add_data[user_lang],
                              reply_markup=K().back(user_lang))
    update.message.reply_document(document=open('static/data.xlsx', 'rb'))
    return S.ADD_DATA


def change_data(path='static/data.xlsx'):
    wb = openpyxl.load_workbook(path)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        category, _ = Categories.objects.get_or_create(title=row[0].value)
        capacity, _ = Capacities.objects.get_or_create(title=row[2].value)
        document, _ = Documents.objects.get_or_create(title=row[5].value)
        country, _ = Countries.objects.get_or_create(title=row[6].value)
        status, _ = Statuses.objects.get_or_create(title=row[7].value)
        memory, _ = Memories.objects.get_or_create(title=row[4].value)
        color, _ = Colors.objects.get_or_create(title=row[3].value)
        producty, _ = Products.objects.get_or_create(title=row[1].value)
        producty.category = category
        if capacity.title != 'Y':
            capacities = producty.capacity.all()
            capacities.append(capacity)
            producty.capacity.set(capacities)
        if color.title != 'Y':
            colors = producty.color.all()
            colors.append(color)
            producty.color.set(colors)
        if memory.title != 'Y':
            memories = producty.memory.all()
            memories.append(memory)
            producty.memory.set(memories)
        if document.title != 'Y':
            documents = producty.document.all()
            documents.append(document)
            producty.document.set(documents)
        if country.title != 'Y':
            countries = producty.country.all()
            countries.append(country)
            producty.country.set(countries)
        if status.title != 'Y':
            statuses = producty.status.all()
            statuses.append(status)
            producty.status.set(statuses)
        producty.price = row[8].value
        producty.save()

    wb.save(path)


def get_data(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return S.START
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file = context.bot.get_file(file_id)
    file.download('static/' + file_name)
    change_data('static/' + file_name)
    update.message.reply_text(T().success[user_lang], reply_markup=K().base(user_lang))
    return S.ADMIN
