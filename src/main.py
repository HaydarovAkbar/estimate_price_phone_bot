import sys

sys.dont_write_bytecode = True

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django

django.setup()
from decouple import config

import logging

TOKEN = config('TOKEN')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

from methods.core.views import start, followers, sale_product, get_category, get_capacity, get_capacity_product, \
    get_color, get_memory, get_document, get_country, get_status, send_admin, change_language, choose_language, \
    report_admin, get_report
from methods.admin.views import admin, add_admin, get_admin_id, get_admins, delete_admin, get_users, add_data, get_data, \
    add_channel, get_channel_name, get_channel_url, get_channel_id, get_channels, delete_channel, get_reklama, \
    send_reklama

from methods.admin.message import KeyboardsAdmin as bt
from methods.core.texts import KeyboardsTexts as msg_txt

from states import States as st

from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler, Updater

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

all_handlers = ConversationHandler(
    entry_points=[
        CommandHandler('start', start),
        CommandHandler('admin', admin)],
    states={
        st.START: [
            CommandHandler('start', start),
            CommandHandler('admin', admin)],

        st.FOLLOWERS: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            CallbackQueryHandler(followers)],

        st.ADMIN: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][0] + ')$'), add_admin),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][1] + ')$'), get_admins),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][2] + ')$'), get_users),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][3] + ')$'), add_data),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][4] + ')$'), add_channel),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][5] + ')$'), get_channels),
            MessageHandler(Filters.regex('^(' + bt.base['uz'][6] + ')$'), get_reklama),

            MessageHandler(Filters.regex('^(' + bt.base['ru'][0] + ')$'), add_admin),
            MessageHandler(Filters.regex('^(' + bt.base['ru'][1] + ')$'), get_admins),
            MessageHandler(Filters.regex('^(' + bt.base['ru'][2] + ')$'), get_users),
            MessageHandler(Filters.regex('^(' + bt.base['ru'][3] + ')$'), add_data),
            MessageHandler(Filters.regex('^(' + bt.base['ru'][4] + ')$'), add_channel),
            MessageHandler(Filters.regex('^(' + bt.base['ru'][5] + ')$'), get_channels),
            MessageHandler(Filters.regex('^(' + bt.base['ru'][6] + ')$'), get_reklama),

            MessageHandler(Filters.regex('^(' + bt.base['en'][0] + ')$'), add_admin),
            MessageHandler(Filters.regex('^(' + bt.base['en'][1] + ')$'), get_admins),
            MessageHandler(Filters.regex('^(' + bt.base['en'][2] + ')$'), get_users),
            MessageHandler(Filters.regex('^(' + bt.base['en'][3] + ')$'), add_data),
            MessageHandler(Filters.regex('^(' + bt.base['en'][4] + ')$'), add_channel),
            MessageHandler(Filters.regex('^(' + bt.base['en'][5] + ')$'), get_channels),
            MessageHandler(Filters.regex('^(' + bt.base['en'][6] + ')$'), get_reklama),
        ],
        st.REKLAMA: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            MessageHandler(Filters.all, send_reklama),
        ],
        st.ADD_CHANNEL: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            MessageHandler(Filters.text, get_channel_name),
        ],
        st.ADD_CHANNEL_URL: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            MessageHandler(Filters.text, get_channel_url),
        ],
        st.ADD_CHANNEL_ID: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            MessageHandler(Filters.text, get_channel_id),
        ],
        st.DELETE_CHANNEL: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            CallbackQueryHandler(delete_channel),
        ],
        st.ADD_ADMIN: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            MessageHandler(Filters.text, get_admin_id),
        ],
        st.ADMINS: [CommandHandler('start', start),
                    CommandHandler('admin', admin),
                    MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
                    MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
                    MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
                    CallbackQueryHandler(delete_admin),
                    ],
        st.ADD_DATA: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
            MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
            MessageHandler(Filters.document, get_data),
        ],
        st.MAIN_MENU: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.main['uz'][0] + ')$'), sale_product),
            MessageHandler(Filters.regex('^(' + msg_txt.main['uz'][1] + ')$'), change_language),
            MessageHandler(Filters.regex('^(' + msg_txt.main['uz'][2] + ')$'), report_admin),

            MessageHandler(Filters.regex('^(' + msg_txt.main['ru'][0] + ')$'), sale_product),
            MessageHandler(Filters.regex('^(' + msg_txt.main['ru'][1] + ')$'), change_language),
            MessageHandler(Filters.regex('^(' + msg_txt.main['ru'][2] + ')$'), report_admin),

            MessageHandler(Filters.regex('^(' + msg_txt.main['en'][0] + ')$'), sale_product),
            MessageHandler(Filters.regex('^(' + msg_txt.main['en'][1] + ')$'), change_language),
            MessageHandler(Filters.regex('^(' + msg_txt.main['en'][2] + ')$'), report_admin),

        ],
        st.SALE_PRODUCT: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), start),

            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_category),
        ],
        st.GET_PRODUCT: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_category),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_category),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_category),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_capacity),
        ],
        st.GET_CAPACITY: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_capacity),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_capacity),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_capacity),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_capacity_product),
        ],
        st.GET_COLOR: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_capacity_product),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_capacity_product),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_capacity_product),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_color),
        ],
        st.GET_MEMORY: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_color),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_color),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_color),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_memory),
        ],
        st.GET_DOCUMENT: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_memory),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_memory),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_memory),

            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),

            MessageHandler(Filters.text, get_document),
        ],
        st.GET_COUNTRY: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_document),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_document),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_document),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_country),
        ],

        st.GET_STATUS: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_country),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_country),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_country),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, get_status),
        ],
        st.SEND_CHANNEL: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), get_country),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), get_country),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), get_country),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back_main['en'] + ')$'), start),
            MessageHandler(Filters.text, send_admin),
        ],
        st.CHOOSE_LANGUAGE: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), start),
            MessageHandler(Filters.text, choose_language),
        ],
        st.REPORT_ADMIN: [
            CommandHandler('start', start),
            CommandHandler('admin', admin),
            MessageHandler(Filters.regex('^(' + msg_txt.back['uz'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back['ru'] + ')$'), start),
            MessageHandler(Filters.regex('^(' + msg_txt.back['en'] + ')$'), start),
            MessageHandler(Filters.all, get_report),
        ],
    },
    fallbacks=[]
)

dispatcher.add_handler(all_handlers)
updater.start_polling()
updater.idle()
print('Bot is running...')
