import sys

sys.dont_write_bytecode = True
# Django specific settings
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()
from decouple import config
# Import your models for use in your script
import logging, pytz

TOKEN = config('TOKEN')
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from methods.core.views import leader, get_report, get_report_week, get_report_month, add_fuel_size, add_fuel_type, \
    add_fuel_price, add_fuel, change_fuel_price, choose_fuel_price, fuel_price_input, get_report_fuel_type
from methods.admin.views import admin, add_organization, get_organization_name, add_user, get_organization_phone, \
    get_organization_address, get_organization_leader, delete_organization, get_organization_id, \
    organization_fuel_types, organization_fuel_columns, get_user_id, get_user_organization, \
    change_user_role, delete_user, get_user_id_delete, add_organization_fuel_column
from methods.kassir.views import send_night_notification, get_start, get_fuel_type, get_naxt_data, \
    get_fuel_column_num, get_plastig_data, get_today_fuel_column, start
from states import States as st
from datetime import time

from methods.kassir.texts import KeyboardsTexts as kas_txt
from methods.core.texts import KeyboardsTexts as core_txt
from methods.dictionary import AdminButton as bt

bt = bt()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True, workers=500)
app = updater.dispatcher

job = updater.job_queue

job.run_daily(send_night_notification, days=(0, 1, 2, 3, 4, 5, 6),
              time=time(hour=23, minute=59, second=00, tzinfo=pytz.timezone('Asia/Tashkent')), )

handler = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CommandHandler('admin', admin),
        CommandHandler('leader', leader),
        MessageHandler(Filters.regex('^(' + kas_txt.start['uz'] + ')$'), get_start),
        MessageHandler(Filters.regex('^(' + kas_txt.start['ru'] + ')$'), get_start),
        MessageHandler(Filters.regex('^(' + kas_txt.start['en'] + ')$'), get_start),
    ],
    states={
        st.NOTSTART: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.start['uz'] + ')$'), get_start),
            MessageHandler(Filters.regex('^(' + kas_txt.start['ru'] + ')$'), get_start),
            MessageHandler(Filters.regex('^(' + kas_txt.start['en'] + ')$'), get_start),
        ],
        st.ADD_TODAY_DATA: [
            CommandHandler('start', start),
            CommandHandler('leader', leader),
            CallbackQueryHandler(get_fuel_type),
        ],
        st.ADD_TODAY_FUEL_COLUMN: [
            CommandHandler('start', start),
            CommandHandler('leader', leader),
            CallbackQueryHandler(get_today_fuel_column),
        ],
        st.NAXT_DATA: [
            CommandHandler('start', start),
            CommandHandler('leader', leader),
            MessageHandler(Filters.text, get_naxt_data)
        ],
        st.PLASTIG_DATA: [
            CommandHandler('start', start),
            CommandHandler('leader', leader),
            MessageHandler(Filters.text, get_plastig_data)
        ],
        st.ADD_FUEL_COLUMN_NUM: [
            CommandHandler('leader', leader),
            MessageHandler(Filters.text, get_fuel_column_num)
        ],

        st.ADMIN: [
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][0] + ')$'), add_user),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][1] + ')$'), add_organization),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][2] + ')$'), delete_organization),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][3] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][4] + ')$'), delete_user),

            MessageHandler(Filters.regex('^(' + bt.adm_menu['ru'][0] + ')$'), add_user),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['ru'][1] + ')$'), add_organization),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['ru'][2] + ')$'), delete_organization),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['ru'][3] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][4] + ')$'), delete_user),

            MessageHandler(Filters.regex('^(' + bt.adm_menu['en'][0] + ')$'), add_user),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['en'][1] + ')$'), add_organization),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['en'][2] + ')$'), delete_organization),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['en'][3] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.adm_menu['uz'][4] + ')$'), delete_user),
        ],
        st.ADD_ORGANIZATION: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            MessageHandler(Filters.text, get_organization_name),
        ],
        st.ADD_ORGANIZATION_PHONE: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            MessageHandler(Filters.text, get_organization_phone),
        ],
        st.ADD_ORGANIZATION_ADDRESS: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            MessageHandler(Filters.text, get_organization_address),
        ],
        st.ADD_ORGANIZATION_LEADER: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            MessageHandler(Filters.text, get_organization_leader),
        ],
        st.ORGANIZATION_FUEL_TYPE: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            CallbackQueryHandler(organization_fuel_types),
        ],
        st.ORGANIZATION_FUEL_COLUMN: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            CallbackQueryHandler(organization_fuel_columns),
        ],
        st.ORGANIZATION_FUEL_COLUMN2: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),

            CallbackQueryHandler(add_organization_fuel_column),
        ],
        st.DELETE_ORGANIZATION: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CommandHandler('leader', leader),
            CallbackQueryHandler(get_organization_id),
        ],
        st.ADD_USER: [CommandHandler('start', start),
                      CommandHandler('admin', admin),
                      CommandHandler('leader', leader),
                      CallbackQueryHandler(get_user_id),
                      ],
        st.CHOOSE_ORGANIZATION: [CommandHandler('start', start),
                                 CommandHandler('admin', admin),
                                 CommandHandler('leader', leader),
                                 CallbackQueryHandler(get_user_organization),
                                 ],

        st.USER_ROLE: [CommandHandler('start', start),
                       CommandHandler('admin', admin),
                       CommandHandler('leader', leader),
                       MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
                       MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
                       MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),
                       CallbackQueryHandler(change_user_role),
                       ],
        st.USER_CONF: [CommandHandler('start', start),
                       CommandHandler('admin', admin),
                       CommandHandler('leader', leader),
                       MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
                       MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
                       MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),
                       MessageHandler(Filters.text, change_user_role),
                       ],
        st.DELETE_USER: [CommandHandler('start', start),
                         CommandHandler('admin', admin),
                         CommandHandler('leader', leader),
                         MessageHandler(Filters.regex('^(' + kas_txt.back['uz'] + ')$'), admin),
                         MessageHandler(Filters.regex('^(' + kas_txt.back['ru'] + ')$'), admin),
                         MessageHandler(Filters.regex('^(' + kas_txt.back['en'] + ')$'), admin),
                         MessageHandler(Filters.text, get_user_id_delete),
                         ],
        st.MAIN_MENU_ADMIN: [CommandHandler('start', start),
                             CommandHandler('admin', admin),
                             CommandHandler('leader', leader),
                             MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                             MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                             MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),

                             MessageHandler(Filters.regex('^(' + core_txt.main['uz'][0] + ')$'), get_report_fuel_type),
                             MessageHandler(Filters.regex('^(' + core_txt.main['uz'][1] + ')$'), add_fuel),
                             MessageHandler(Filters.regex('^(' + core_txt.main['uz'][2] + ')$'), change_fuel_price),
                             MessageHandler(Filters.regex('^(' + core_txt.main['uz'][3] + ')$'), get_report_fuel_type),

                             MessageHandler(Filters.regex('^(' + core_txt.main['ru'][0] + ')$'), admin),
                             MessageHandler(Filters.regex('^(' + core_txt.main['ru'][1] + ')$'), add_fuel),
                             MessageHandler(Filters.regex('^(' + core_txt.main['ru'][2] + ')$'), change_fuel_price),
                             MessageHandler(Filters.regex('^(' + core_txt.main['ru'][3] + ')$'), admin),

                             MessageHandler(Filters.regex('^(' + core_txt.main['en'][0] + ')$'), admin),
                             MessageHandler(Filters.regex('^(' + core_txt.main['en'][1] + ')$'), add_fuel),
                             MessageHandler(Filters.regex('^(' + core_txt.main['en'][2] + ')$'), change_fuel_price),
                             MessageHandler(Filters.regex('^(' + core_txt.main['en'][3] + ')$'), admin),
                             ],
        st.GET_REPORT_FUEL_TYPE: [CommandHandler('start', start),
                                  CommandHandler('leader', leader),
                                  MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                                  MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                                  MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),
                                  CallbackQueryHandler(get_report),
                                  ],
        st.GET_REPORT: [CommandHandler('start', start),
                        CommandHandler('admin', admin),
                        CommandHandler('leader', leader),
                        MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                        MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                        MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),

                        MessageHandler(Filters.regex('^(' + core_txt.report['uz'][0] + ')$'), get_report_week),
                        MessageHandler(Filters.regex('^(' + core_txt.report['uz'][1] + ')$'), get_report_month),
                        MessageHandler(Filters.regex('^(' + core_txt.report['ru'][0] + ')$'), get_report_week),
                        MessageHandler(Filters.regex('^(' + core_txt.report['ru'][1] + ')$'), get_report_month),
                        MessageHandler(Filters.regex('^(' + core_txt.report['en'][0] + ')$'), get_report_week),
                        MessageHandler(Filters.regex('^(' + core_txt.report['en'][1] + ')$'), get_report_month),
                        ],
        st.ADD_FUEL: [CommandHandler('start', start),
                      CommandHandler('leader', leader),
                      MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                      MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                      MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),
                      MessageHandler(Filters.text, add_fuel_size),
                      ],
        st.ADD_FUEL_TYPE: [CommandHandler('start', start),
                           CommandHandler('leader', leader),
                           MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                           MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                           MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),
                           CallbackQueryHandler(add_fuel_type),
                           ],
        st.ADD_FUEL_PRICE: [CommandHandler('start', start),
                            CommandHandler('leader', leader),
                            MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                            MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                            MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),
                            MessageHandler(Filters.text, add_fuel_price),
                            ],
        st.CHANGE_FUEL_PRICE: [CommandHandler('start', start),
                               CommandHandler('leader', leader),
                               MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                               MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                               MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),
                               CallbackQueryHandler(choose_fuel_price),
                               ],
        st.FUEL_PRICE_INPUT: [CommandHandler('start', start),
                              CommandHandler('leader', leader),
                              MessageHandler(Filters.regex('^(' + core_txt.back['uz'] + ')$'), leader),
                              MessageHandler(Filters.regex('^(' + core_txt.back['ru'] + ')$'), leader),
                              MessageHandler(Filters.regex('^(' + core_txt.back['en'] + ')$'), leader),
                              MessageHandler(Filters.text, fuel_price_input),
                              ],
    },
    fallbacks=[
        CommandHandler('start', start),
        CommandHandler('leader', leader),

        MessageHandler(Filters.regex('^(' + kas_txt.start['uz'] + ')$'), get_start),
        MessageHandler(Filters.regex('^(' + kas_txt.start['ru'] + ')$'), get_start),
        MessageHandler(Filters.regex('^(' + kas_txt.start['en'] + ')$'), get_start),
    ]
)

app.add_handler(handler=handler)

updater.start_polling()
print('started polling')
updater.idle()
