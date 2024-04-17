from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CallbackContext
from states import States as S
from db.models import User, Organization, FuelType, FuelColumn, FuelStorage, FuelColumnPointer, \
    OrganizationFuelTypes, OrganizationFuelColumns
from .keyboards import KeyboardsAdmin as K
from ..dictionary import AdmTexts as T


def admin(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_text(T().start[user_lang].format(tg_user.full_name),
                              reply_markup=K().get_admin_menu(user_lang))
    return S.ADMIN


def add_organization(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.get(chat_id=tg_user.id, is_active=True)
    if not user.is_admin:
        return 1
    user_lang = user.language if user.language else 'uz'
    update.message.reply_html(T().add_organization[user_lang], reply_markup=K().back(user_lang))
    return S.ADD_ORGANIZATION


def get_organization_name(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.get(chat_id=tg_user.id, is_active=True)
    if not user.is_admin:
        return 1
    user_lang = user.language if user.language else 'uz'
    context.chat_data['organ_name'] = update.message.text
    update.message.reply_html(T().add_organ_phone[user_lang], reply_markup=K().back(user_lang))
    return S.ADD_ORGANIZATION_PHONE


def get_organization_phone(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.get(chat_id=tg_user.id, is_active=True)
    if not user.is_admin:
        return 1
    user_lang = user.language if user.language else 'uz'
    context.chat_data['organ_phone'] = update.message.text
    update.message.reply_html(T().add_organ_address[user_lang], reply_markup=K().back(user_lang))
    return S.ADD_ORGANIZATION_ADDRESS


def get_organization_address(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.get(chat_id=tg_user.id, is_active=True)
    if not user.is_admin:
        return 1
    user_lang = user.language if user.language else 'uz'
    context.chat_data['organ_address'] = update.message.text
    update.message.reply_html(T().add_organ_leader[user_lang], reply_markup=K().back(user_lang))
    return S.ADD_ORGANIZATION_LEADER


def get_organization_leader(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.get(chat_id=tg_user.id, is_active=True)
    if not user.is_admin:
        return 1
    user_lang = user.language if user.language else 'uz'
    context.chat_data['organ_leader'] = update.message.text
    organ, _ = Organization.objects.get_or_create(
        title=context.chat_data['organ_name'],
        phone=context.chat_data['organ_phone'],
        address=context.chat_data['organ_address'],
        leader=context.chat_data['organ_leader']
    )
    fuel_types = FuelType.objects.filter(is_active=True)
    context.chat_data['organization'] = organ
    context.chat_data['selected'] = []
    update.message.reply_html(T().organization_added[user_lang],
                              reply_markup=K().organ_fuel_column(fuel_types, []))
    return S.ORGANIZATION_FUEL_TYPE


def organization_fuel_types(update: Update, context: CallbackContext):
    query = update.callback_query
    user_db = User.objects.get(chat_id=query.from_user.id)
    if query.data == 'confirm':
        query.delete_message()
        selected = context.chat_data.get('selected', [])
        organization = context.chat_data.get('organization')
        for fuel in selected:
            fuel_type = FuelType.objects.get(id=fuel)
            OrganizationFuelTypes.objects.create(organization=organization, fuel_type=fuel_type)
        fuel_columns = FuelColumn.objects.filter(is_active=True)
        context.chat_data['selected'] = []
        organ_fuel_types = OrganizationFuelTypes.objects.filter(organization=context.chat_data['organization'])
        context.chat_data['organ_fuel_types'] = {str(i.fuel_type.id): False for i in organ_fuel_types}
        fuel_type_first = organ_fuel_types.first().fuel_type
        query.message.reply_html(T().add_organ_fuel_column[user_db.language].format(fuel_type_first.title),
                                 reply_markup=K().organ_fuel_column(fuel_columns, []))
        return S.ORGANIZATION_FUEL_COLUMN
    selected = context.chat_data.get('selected', [])
    if query.data in selected:
        selected.remove(query.data)
    else:
        selected.append(query.data)
    fuel_types = FuelType.objects.filter(is_active=True)
    context.chat_data['selected'] = selected
    query.edit_message_text(text=T().again_enter_fuel_type[user_db.language], parse_mode='HTML',
                            reply_markup=K().organ_fuel_column(fuel_types, selected))
    return S.ORGANIZATION_FUEL_TYPE


def organization_fuel_columns(update: Update, context: CallbackContext):
    query = update.callback_query
    user_db = User.objects.get(chat_id=query.from_user.id)
    organ_fuel_types = context.chat_data.get('organ_fuel_types')
    first_fuel_type = list(organ_fuel_types.keys())[0]
    fuel_type_first = FuelType.objects.get(id=first_fuel_type)
    if query.data == 'confirm':
        query.delete_message()
        selected = context.chat_data.get('selected', [])
        organization = context.chat_data.get('organization')
        for fuel in selected:
            fuel_column = FuelColumn.objects.get(id=fuel)
            OrganizationFuelColumns.objects.create(organization=organization, fuel_column=fuel_column,
                                                   fuel_type=fuel_type_first)
        context.chat_data['selected'] = []
        organ_fuel_types[first_fuel_type] = True
        secound_fuel_type = list(organ_fuel_types.keys())[1] if len(organ_fuel_types) > 1 else None
        if secound_fuel_type and not organ_fuel_types[secound_fuel_type]:
            context.chat_data['organ_fuel_types'] = organ_fuel_types
            fuel_type_secound = FuelType.objects.get(id=secound_fuel_type)
            fuel_columns = FuelColumn.objects.filter(is_active=True)
            query.message.reply_html(T().add_organ_fuel_column[user_db.language].format(fuel_type_secound.title),
                                     reply_markup=K().organ_fuel_column(fuel_columns, []))
            return S.ORGANIZATION_FUEL_COLUMN2

        query.message.reply_html(T().added_organization[user_db.language],
                                 reply_markup=K().get_admin_menu(user_db.language))
        return S.ADMIN
    selected = context.chat_data.get('selected', [])
    if query.data in selected:
        selected.remove(query.data)
    else:
        selected.append(query.data)
    fuel_columns = FuelColumn.objects.filter(is_active=True)
    context.chat_data['selected'] = selected
    query.edit_message_text(text=T().add_organ_fuel_column[user_db.language].format(fuel_type_first), parse_mode='HTML',
                            reply_markup=K().organ_fuel_column(fuel_columns, selected))

    return S.ORGANIZATION_FUEL_COLUMN


def add_organization_fuel_column(update: Update, context: CallbackContext):
    query = update.callback_query
    user_db = User.objects.get(chat_id=query.from_user.id)
    organ_fuel_types = context.chat_data.get('organ_fuel_types')
    fuel_type = False
    for key, value in organ_fuel_types.items():
        if not value:
            fuel_type = FuelType.objects.get(id=key)
            break
    if not fuel_type:
        query.delete_message()
        query.message.reply_html(T().added_organization[user_db.language],
                                 reply_markup=K().get_admin_menu(user_db.language))
        return S.ADMIN
    if query.data == 'confirm':
        query.delete_message()
        selected = context.chat_data.get('selected', [])
        organization = context.chat_data.get('organization')
        for fuel in selected:
            fuel_column = FuelColumn.objects.get(id=fuel)
            OrganizationFuelColumns.objects.create(organization=organization, fuel_column=fuel_column,
                                                   fuel_type=fuel_type)
        context.chat_data['selected'] = []
        organ_fuel_types[str(fuel_type.id)] = True
        secound_fuel_type = False
        for key, value in organ_fuel_types.items():
            if not value:
                secound_fuel_type = FuelType.objects.get(id=key)
                break
        if not secound_fuel_type:
            query.message.reply_html(T().added_organization[user_db.language],
                                     reply_markup=K().get_admin_menu(user_db.language))
            return S.ADMIN
        if secound_fuel_type and not organ_fuel_types[str(secound_fuel_type.id)]:
            context.chat_data['organ_fuel_types'] = organ_fuel_types
            fuel_columns = FuelColumn.objects.filter(is_active=True)
            query.message.reply_html(T().add_organ_fuel_column[user_db.language].format(secound_fuel_type.title),
                                     reply_markup=K().organ_fuel_column(fuel_columns, []))
            return S.ORGANIZATION_FUEL_COLUMN2

        query.message.reply_html(T().added_organization[user_db.language],
                                 reply_markup=K().get_admin_menu(user_db.language))
        return S.ADMIN
    selected = context.chat_data.get('selected', [])
    if query.data in selected:
        selected.remove(query.data)
    else:
        selected.append(query.data)
    fuel_columns = FuelColumn.objects.filter(is_active=True)
    context.chat_data['selected'] = selected
    query.edit_message_text(text=T().add_organ_fuel_column[user_db.language].format(fuel_type), parse_mode='HTML',
                            reply_markup=K().organ_fuel_column(fuel_columns, selected))

    return S.ORGANIZATION_FUEL_COLUMN2


def delete_organization(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.get(chat_id=tg_user.id, is_active=True)
    if not user.is_admin:
        return 1
    user_lang = user.language if user.language else 'uz'
    organization = Organization.objects.filter(is_active=True)
    update.message.reply_html(T().delete_organization[user_lang], reply_markup=K().organization_list(organization))
    return S.DELETE_ORGANIZATION


def get_organization_id(update: Update, context: CallbackContext):
    query = update.callback_query
    user = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user.language if user.language else 'uz'
    organization_id = query.data
    if organization_id == 'back':
        query.delete_message()
        context.bot.send_message(chat_id=query.from_user.id, text=T().start[user_lang].format(user.fullname),
                                 reply_markup=K().get_admin_menu(user_lang))
        return S.ADMIN
    organization = Organization.objects.get(id=organization_id)
    query.delete_message()
    organization.is_active = False
    organization.save()
    query.message.reply_html(T().delete_organization_success[user_lang], reply_markup=K().get_admin_menu())
    return S.ADMIN


def get_users(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_html(T().get_user[user_lang],
                              reply_markup=K().get_user_menu(user_lang))
    return S.GET_USERS


def settings(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_html(T().get_user[user_lang], reply_markup=K().adm_settings(user_lang))
    return S.ADMIN_SETTINGS


def change_language(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_html(T().change_language[user_lang], reply_markup=K().get_lang())
    return S.CHANGE_LANG


def get_lang(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer(text="Til o'zgartirildi: {}".format(query.data))
    change_lang = query.data
    user = User.objects.get(chat_id=query.from_user.id)
    user.language = change_lang
    user.save()
    query.message.delete(timeout=1)
    tg_user = query.from_user
    context.bot.send_message(chat_id=query.from_user.id, text=T().start[change_lang].format(tg_user.full_name),
                             reply_markup=K().get_admin_menu(change_lang))
    return S.ADMIN


def back(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_text(T().start[user_lang].format(tg_user.full_name),
                              reply_markup=K().get_admin_menu(user_lang))
    return S.ADMIN


def add_user(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    user_list = User.objects.filter(is_active=False).order_by('-created_at')[0:10]
    update.message.reply_text('...', reply_markup=ReplyKeyboardRemove())
    update.message.reply_html(T().add_user[user_lang], reply_markup=K().user_list(user_list))
    return S.ADD_USER


def get_user_id(update: Update, context: CallbackContext):
    query = update.callback_query
    user_id = query.data
    user_db = User.objects.get(chat_id=query.from_user.id)
    query.delete_message()
    if user_id == 'back':
        context.bot.send_message(chat_id=query.from_user.id, text=T().start[user_db.language].format(user_db.fullname),
                                 reply_markup=K().get_admin_menu(user_db.language))
        return S.ADMIN
    context.chat_data['user_id'] = user_id
    organizations = Organization.objects.filter(is_active=True)
    context.bot.send_message(chat_id=query.from_user.id,
                             text=T().choose_organization[user_db.language],
                             parse_mode='HTML',
                             reply_markup=K().organization_list(organizations))
    return S.CHOOSE_ORGANIZATION


def get_user_organization(update: Update, context: CallbackContext):
    query = update.callback_query
    user_db = User.objects.get(chat_id=update.effective_user.id)
    user_lang = user_db.language if user_db.language else 'uz'
    organization_id = query.data
    if organization_id == 'back':
        query.delete_message()
        context.bot.send_message(chat_id=query.from_user.id, text=T().start[user_lang].format(user_db.fullname),
                                 reply_markup=K().get_admin_menu(user_lang))
        return S.ADMIN
    organization = Organization.objects.get(id=organization_id)
    user = User.objects.get(chat_id=context.chat_data['user_id'])
    user.organization = organization
    user.save()
    query.delete_message()
    query.message.reply_html(T().roles[user_lang], reply_markup=K().roles(user_lang))
    return S.USER_ROLE


def change_user(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    user_list = User.objects.filter(state__id=1).order_by('-created_at')[0:20]
    update.message.reply_text('...', reply_markup=ReplyKeyboardRemove())
    update.message.reply_html(T().add_user[user_lang], reply_markup=K().user_list(user_list))
    return S.CHANGED_USER


def change_user_role(update: Update, context: CallbackContext):
    query = update.callback_query
    user_db = User.objects.get(chat_id=query.from_user.id)
    user_lang = user_db.language if user_db.language else 'uz'
    user_id = context.chat_data['user_id']
    user = User.objects.get(chat_id=user_id)
    if query.data == 'back':
        query.delete_message()
        context.bot.send_message(chat_id=query.from_user.id, text=T().start[user_lang].format(user_db.fullname),
                                 reply_markup=K().get_admin_menu(user_lang))
        return S.ADMIN
    if query.data == 'delete':
        user.delete()
        query.delete_message()
        context.bot.send_message(chat_id=query.from_user.id, text=T().user_deleted[user_lang], parse_mode='HTML',
                                 reply_markup=K().get_admin_menu(user_lang))
        return S.ADMIN
    role = query.data
    if role == 'leader':
        user.is_leader = True
        user.is_active = True
    elif role == 'cashier':
        user.is_cashier = True
        user.is_active = True
    elif role == 'leader_cashier':
        user.is_leader = True
        user.is_cashier = True
        user.is_active = True
    user.save()
    query.delete_message()
    context.bot.send_message(chat_id=query.from_user.id, text=T().user_added[user_lang], parse_mode='HTML',
                             reply_markup=K().get_admin_menu(user_lang))
    return S.ADMIN


def delete_user(update: Update, context: CallbackContext):
    tg_user = update.message.from_user
    user = User.objects.filter(chat_id=tg_user.id, is_active=True, is_admin=True)
    if not user.exists():
        return 1
    user = user.first()
    user_lang = user.language if user.language else 'uz'
    update.message.reply_html(T().delete_user[user_lang], reply_markup=K().back(user_lang))
    return S.DELETE_USER


def get_user_id_delete(update: Update, context: CallbackContext):
    user_id = update.message.text
    user_db = User.objects.get(chat_id=update.effective_user.id)
    if not user_id.isdigit() or not User.objects.filter(chat_id=user_id).exists():
        update.message.reply_html(T().wrong_id[user_db.language], reply_markup=K().back(user_db.language))
        return S.DELETE_USER
    context.chat_data['user_id'] = user_id
    user_new = User.objects.get(chat_id=user_id)
    user_lang = user_db.language
    user_role = ''
    if user_new.is_leader and user_new.is_cashier:
        user_role = 'leader_cashier'
    elif user_new.is_leader:
        user_role = 'leader'
    elif user_new.is_cashier:
        user_role = 'cashier'
    context.bot.send_message(chat_id=user_db.chat_id,
                             text=T().change_user[user_lang].format(user_new.fullname), parse_mode='HTML',
                             reply_markup=K().roles(user_role, user_lang))
    return S.USER_ROLE
