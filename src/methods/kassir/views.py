from telegram.ext import CallbackContext
from telegram import Update, ReplyKeyboardRemove
from django.utils import timezone
from django.db.models import Sum

from .texts import MessageTexts as msg_txt
from .keryboards import KassirKeyboards as kb
from .report import generate_pdf

from db.models import User, FuelColumn, FuelType, PaymentType, OrganizationFuelTypes, SaleFuel, \
    FuelPrice, FuelStorage, FuelStorageHistory, OrganizationFuelColumns, FuelColumnPointer
from states import States as st


def start(update: Update, context: CallbackContext):
    user = User.objects.filter(chat_id=update.effective_user.id, is_active=True, is_cashier=True)
    if user.exists():
        user = user.first()
        update.message.reply_html(
            f"Salom, {user.fullname}!\n"
            f"Hisobot kiritish uchun. Bot sizga bildirishnoma yuborishini kuting!"
        )
        return 1
    else:
        user, _ = User.objects.get_or_create(chat_id=update.effective_user.id,
                                             defaults={'username': update.effective_user.username,
                                                       'fullname': update.effective_user.full_name
                                                       })


def send_night_notification(context: CallbackContext):
    users = User.objects.filter(is_active=True, is_cashier=True)
    for user in users:
        try:
            context.bot.send_message(
                chat_id=user.chat_id,
                text=msg_txt.start_notification[user.language],
                reply_markup=kb.start(user.language)
            )
        except Exception:
            pass
    return st.NOTSTART


def get_start(update: Update, context: CallbackContext):
    user, _ = User.objects.get_or_create(chat_id=update.effective_user.id,
                                         defaults={'username': update.effective_user.username,
                                                   'fullname': update.effective_user.full_name
                                                   })
    if user and user.is_active:
        update.message.reply_html(msg_txt.lets_start[user.language], reply_markup=ReplyKeyboardRemove())
        organization_fuel_types = OrganizationFuelTypes.objects.filter(organization=user.organization)
        msg, i = "", 0
        for org_fuel_type in organization_fuel_types:
            fuel_data = SaleFuel.objects.filter(fuel_type=org_fuel_type.fuel_type, organization=user.organization,
                                                created_at__date=timezone.now().date())
            if fuel_data:
                i += 1
                msg += f"{org_fuel_type.fuel_type.title} - ✅\n"
            else:
                msg += f"{org_fuel_type.fuel_type.title} ❗️\n"
        if i == organization_fuel_types.count():
            return fuel_column_pointer(update, context)
        user_fuel_type_txt = f"""
<b>{user.fullname}</b> - <code>{user.organization.title}</code> tashkiloti uchun:

<i>Bugungi hisobotlarni kiriting</i>

{msg}
Yuqoridagi yoqilg'ilar uchun ma'lumotlar kiritish uchun pastdagi tugmalardan birini tanlang 👇
"""
        update.message.reply_html(text=user_fuel_type_txt,
                                  reply_markup=kb.organ_fuel_types(organization_fuel_types, user.language))
        return st.ADD_TODAY_DATA


def get_fuel_type(update: Update, context: CallbackContext):
    query = update.callback_query
    fuel_type = FuelType.objects.get(id=update.callback_query.data)
    context.user_data['fuel_type'] = fuel_type
    query.delete_message()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="<code>Bugungi naxt holatdagi savdo hajmini kiriting</code> [litr]",
                             parse_mode='HTML')
    return st.NAXT_DATA


def get_naxt_data(update: Update, context: CallbackContext):
    data_size = update.message.text
    if data_size.isdigit() and int(data_size) >= 0:
        context.user_data['naxt_data_size'] = int(data_size)
        update.message.reply_html(
            text="<code>Bugungi plastig holatdagi savdo hajmini kiriting</code> [litr]"
        )
        return st.PLASTIG_DATA
    else:
        update.message.reply_text(
            text="<code>Bugungi naxt holatdagi savdo hajmini kiriting</code>",
            parse_mode='HTML'
        )


def fuel_column_pointer(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    fuel_type = context.user_data['fuel_type']
    fuel_columns = OrganizationFuelColumns.objects.filter(organization=user.organization, fuel_type=fuel_type)
    if not fuel_columns:
        organization_fuel_types = OrganizationFuelTypes.objects.filter(organization=user.organization)
        msg, i = "", 0
        for org_fuel_type in organization_fuel_types:
            fuel_data = SaleFuel.objects.filter(fuel_type=org_fuel_type.fuel_type, organization=user.organization,
                                                created_at__date=timezone.now().date())
            if fuel_data:
                i += 1
                msg += f"{org_fuel_type.fuel_type.title} - ✅\n"
            else:
                msg += f"{org_fuel_type.fuel_type.title} ❗️\n"
        if i == organization_fuel_types.count():
            update.message.reply_html(
                text="<code>Ma'lumotlar saqlab qo'yildi</code>"
            )
            generate_pdf(user)
            update.message.reply_document(
                document=open('static/output.pdf', 'rb'),
                caption="Bugungi hisobot [PDF]"
            )
            return st.FINISHED
        user_fuel_type_txt = f"""
<b>{user.fullname}</b> - <code>{user.organization.title}</code> tashkiloti uchun:

<i>Bugungi hisobotlarni kiriting</i>

{msg}
Yuqoridagi yoqilg'ilar uchun ma'lumotlar kiritish uchun pastdagi tugmalardan birini tanlang 👇
        """
        update.message.reply_html(text=user_fuel_type_txt,
                                  reply_markup=kb.organ_fuel_types(organization_fuel_types, user.language))
        return st.ADD_TODAY_DATA
    msg, i = "", 0
    for fuel_col in fuel_columns:
        fuel_data = FuelColumnPointer.objects.filter(organ=user.organization, fuel_column=fuel_col.fuel_column, fuel_type=fuel_type,
                                                     created_at__date=timezone.now().date())
        if fuel_data:
            i += 1
            msg += f"{fuel_col.fuel_column.title} - ✅\n"
        else:
            msg += f"{fuel_col.fuel_column.title} ❗️\n"
    # if i == fuel_columns.count():
    #     leaders = User.objects.filter(organization=user.organization, is_leader=True)
    #     sale_fuels = SaleFuel.objects.filter(created_at__date=timezone.now().date(), organization=user.organization)
    #     report_msg = (f"<i>Hisobotlar:</i>\n "
    #                   f"{''.join([f'{i + 1}) {sale_fuel.fuel_type.title}: {sale_fuel.price}  ,' for i, sale_fuel in enumerate(sale_fuels)])}")
    #         leader_msg = f"""
    # <b>{user.organization.title}</b> tashkiloti uchun bugungi hisobotlar kiritildi.
    #
    # {report_msg}
    # """
    #         for leader in leaders:
    #             try:
    #                 context.bot.send_message(chat_id=leader.chat_id, text=leader_msg, parse_mode='HTML')
    #             except Exception:
    #                 pass
    #         update.message.reply_html(
    #             text="<code>Yakunlandi!</code>"
    #         )
    #         generate_pdf(user)
    #         update.message.reply_document(
    #             document=open('static/output.pdf', 'rb'),
    #             caption="Bugungi hisobot [PDF]"
    #         )
    #         return st.FINISHED
    user_fuel_column_txt = f"""
<b>{user.fullname}</b> - <code>{user.organization.title}</code> tashkiloti uchun:

<i>Bugungi hisobotlarni kiriting</i>

{msg}
Yuqoridagi yoqilg'i ustunlari uchun ma'lumotlar kiritish uchun pastdagi tugmalardan birini tanlang 👇
                """
    update.message.reply_html(text=user_fuel_column_txt,
                              reply_markup=kb.organ_fuel_columns(fuel_columns, user.language))
    return st.ADD_TODAY_FUEL_COLUMN


def get_today_fuel_column(update: Update, context: CallbackContext):
    query = update.callback_query
    fuel_column = FuelColumn.objects.get(id=query.data)
    context.user_data['fuel_column'] = fuel_column
    query.delete_message()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"<code>Kun oxiridagi {fuel_column.title} - kolonka raqamini kiriting</code>",
                             parse_mode='HTML')
    return st.ADD_FUEL_COLUMN_NUM


def get_fuel_column_num(update: Update, context: CallbackContext):
    user = User.objects.get(chat_id=update.effective_user.id)
    msg = update.message.text
    if msg.isdigit() and int(msg) > 0:
        msg = int(msg)
        context.user_data['column_num'] = msg
        fuel_column = context.user_data['fuel_column']
        fuel_type = context.user_data['fuel_type']
        last_pointer = FuelColumnPointer.objects.filter(organ=user.organization, fuel_column=fuel_column,  fuel_type=fuel_type).order_by(
            'created_at').last()
        FuelColumnPointer.objects.create(
            organ=user.organization,
            fuel_column=fuel_column,
            size_last=float(msg),
            fuel_type=fuel_type,
            size_first=last_pointer.size_last if last_pointer else float(msg),
        )
        fuel_type = context.user_data['fuel_type']
        fuel_columns = OrganizationFuelColumns.objects.filter(organization=user.organization, fuel_type=fuel_type)
        msg, i = "", 0
        for fuel_col in fuel_columns:
            fuel_data = FuelColumnPointer.objects.filter(organ=user.organization, fuel_column=fuel_col.fuel_column, fuel_type=fuel_type,
                                                         created_at__date=timezone.now().date())
            if fuel_data:
                i += 1
                msg += f"{fuel_col.fuel_column.title} - ✅\n"
            else:
                msg += f"{fuel_col.fuel_column.title} ❗️\n"
        if i == fuel_columns.count():

            organization_fuel_types = OrganizationFuelTypes.objects.filter(organization=user.organization)
            msg, i = "", 0
            for org_fuel_type in organization_fuel_types:
                fuel_data = SaleFuel.objects.filter(fuel_type=org_fuel_type.fuel_type, organization=user.organization,
                                                    created_at__date=timezone.now().date())
                if fuel_data:
                    i += 1
                    msg += f"{org_fuel_type.fuel_type.title} - ✅\n"
                else:
                    msg += f"{org_fuel_type.fuel_type.title} ❗️\n"
            if i == organization_fuel_types.count():
                leaders = User.objects.filter(organization=user.organization, is_leader=True)
                sale_fuels = SaleFuel.objects.filter(created_at__date=timezone.now().date(),
                                                     organization=user.organization)
                report_msg = (f"<i>Hisobotlar:</i>\n "
                              f"{''.join([f'{i + 1}) {sale_fuel.fuel_type.title}: {sale_fuel.price}  ,' for i, sale_fuel in enumerate(sale_fuels)])}")
                leader_msg = f"""
                            <b>{user.organization.title}</b> tashkiloti uchun bugungi hisobotlar kiritildi.

                            {report_msg}
                            """
                for leader in leaders:
                    try:
                        context.bot.send_message(chat_id=leader.chat_id, text=leader_msg, parse_mode='HTML')
                    except Exception:
                        pass
                update.message.reply_html(
                    text="<code>Yakunlandi!</code>",
                )
                generate_pdf(user)
                update.message.reply_document(
                    document=open('static/output.pdf', 'rb'),
                    caption="Bugungi hisobot [PDF]"
                )
                return st.FINISHED
                # return fuel_column_pointer(update, context)

            user_fuel_type_txt = f"""
<b>{user.fullname}</b> - <code>{user.organization.title}</code> tashkiloti uchun:

<i>Bugungi hisobotlarni kiriting</i>

{msg}
Yuqoridagi yoqilg'ilar uchun ma'lumotlar kiritish uchun pastdagi tugmalardan birini tanlang 👇
            """
            update.message.reply_html(text=user_fuel_type_txt,
                                      reply_markup=kb.organ_fuel_types(organization_fuel_types, user.language))
            return st.ADD_TODAY_DATA

            # leaders = User.objects.filter(organization=user.organization, is_leader=True)
            # sale_fuels = SaleFuel.objects.filter(created_at__date=timezone.now().date(), organization=user.organization)
            # report_msg = (f"<i>Hisobotlar:</i>\n "
            #               f"{''.join([f'{i + 1}) {sale_fuel.fuel_type.title}: {sale_fuel.price}  ,' for i, sale_fuel in enumerate(sale_fuels)])}")
            # leader_msg = f"""
            # <b>{user.organization.title}</b> tashkiloti uchun bugungi hisobotlar kiritildi.
            #
            # {report_msg}
            # """
            # for leader in leaders:
            #     try:
            #         context.bot.send_message(chat_id=leader.chat_id, text=leader_msg, parse_mode='HTML')
            #     except Exception:
            #         pass
            # update.message.reply_html(
            #     text="<code>Yakunlandi!</code>",
            # )
            # generate_pdf(user)
            # update.message.reply_document(
            #     document=open('static/output.pdf', 'rb'),
            #     caption="Bugungi hisobot [PDF]"
            # )
            # return st.FINISHED
        user_fuel_column_txt = f"""
<b>{user.fullname}</b> - <code>{user.organization.title}</code> tashkiloti uchun:

<i>Bugungi hisobotlarni kiriting</i>

{msg}
Yuqoridagi yoqilg'i ustunlari uchun ma'lumotlar kiritish uchun pastdagi tugmalardan birini tanlang 👇

        """
        update.message.reply_html(text=user_fuel_column_txt,
                                  reply_markup=kb.organ_fuel_columns(fuel_columns, user.language))
        return st.ADD_TODAY_FUEL_COLUMN
    else:
        update.message.reply_text(
            text="<code>Kun oxiridagi kolonka raqamini kiriting</code>",
            parse_mode='HTML'
        )


def get_plastig_data(update: Update, context: CallbackContext):
    data_size = update.message.text
    user = User.objects.get(chat_id=update.effective_user.id)
    if data_size.isdigit() and int(data_size) >= 0:
        data_size = int(data_size)
        context.user_data['plastig_data_size'] = data_size
        naxt_data_size = context.user_data['naxt_data_size']
        fuel_type = context.user_data['fuel_type']
        if FuelPrice.objects.filter(fuel_type=fuel_type, organization=user.organization).exists():
            price = (float(naxt_data_size) + float(data_size)) * FuelPrice.objects.filter(fuel_type=fuel_type,
                                                                                          organization=user.organization).last().price
        else:
            update.message.reply_html(text="<code>Ushbu tashkilot uchun narx kiritilmagan</code>")
            return st.FINISHED
        fuel_stroges = FuelStorage.objects.filter(fuel_type=fuel_type, is_over=False).order_by('created_at')
        if not fuel_stroges:
            update.message.reply_html(
                text="<code>Ushbu tashkilot uchun yoqilg'i kiritilmagan</code>"
            )
            return st.FINISHED
        benefit, counter = 0, naxt_data_size + data_size
        begin = fuel_stroges.aggregate(total=Sum('residual'))['total']
        for fuel_stroge in fuel_stroges:
            if fuel_stroge.residual >= counter:
                benefit = price - fuel_stroge.price * (counter)
                fuel_stroge.residual -= counter
                fuel_stroge.save()
                break
            else:
                counter = counter - fuel_stroge.residual
                benefit += fuel_stroge.price * fuel_stroge.residual
                fuel_stroge.residual = 0
                fuel_stroge.is_over = True
                fuel_stroge.save()
        FuelStorageHistory.objects.create(
            fuel_type=fuel_type,
            begin=begin,
            end=begin - counter,
            organization=user.organization
        )
        SaleFuel.objects.create(
            fuel_type=fuel_type,
            cash_size=float(naxt_data_size),
            card_size=float(data_size),
            price=price,
            benefit=float(benefit),
            organization=user.organization
        )
        organization_fuel_types = OrganizationFuelTypes.objects.filter(organization=user.organization)
        msg, i = "", 0
        for org_fuel_type in organization_fuel_types:
            fuel_data = SaleFuel.objects.filter(fuel_type=org_fuel_type.fuel_type, organization=user.organization,
                                                created_at__date=timezone.now().date())
            if fuel_data:
                i += 1
                msg += f"{org_fuel_type.fuel_type.title} - ✅\n"
            else:
                msg += f"{org_fuel_type.fuel_type.title} ❗️\n"

        return fuel_column_pointer(update, context)

        # if i == organization_fuel_types.count():
        #     return fuel_column_pointer(update, context)

#         user_fuel_type_txt = f"""
# <b>{user.fullname}</b> - <code>{user.organization.title}</code> tashkiloti uchun:
#
# <i>Bugungi hisobotlarni kiriting</i>
#
# {msg}
# Yuqoridagi yoqilg'ilar uchun ma'lumotlar kiritish uchun pastdagi tugmalardan birini tanlang 👇
#         """
#         update.message.reply_html(text=user_fuel_type_txt,
#                                   reply_markup=kb.organ_fuel_types(organization_fuel_types, user.language))
#         return st.ADD_TODAY_DATA
#     else:
#         update.message.reply_text(
#             text="<code>Bugungi plastig holatdagi savdo hajmini kiriting</code>",
#             parse_mode='HTML'
#         )
