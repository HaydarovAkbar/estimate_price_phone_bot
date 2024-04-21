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

from methods.core.views import start, followers
from methods.admin.views import admin, add_admin, get_admin_id, get_admins, delete_admin, get_users, add_data, get_data

from methods.admin.message import KeyboardsAdmin as bt

from states import States as st

from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler, Updater

updater = Updater(token=TOKEN, use_context=True)

dispatcher = updater.dispatcher

all_handlers = ConversationHandler(
    entry_points=[CommandHandler('start', start), CommandHandler('admin', admin)],
    states={
        st.START: [CommandHandler('start', start), CommandHandler('admin', admin)],

        st.FOLLOWERS: [CommandHandler('start', start), CommandHandler('admin', admin),
                       CallbackQueryHandler(followers)],

        st.ADMIN: [CommandHandler('start', start),
                   CommandHandler('admin', admin),
                   MessageHandler(Filters.regex('^(' + bt.base['uz'][0] + ')$'), add_admin),
                   MessageHandler(Filters.regex('^(' + bt.base['uz'][1] + ')$'), get_admins),
                   MessageHandler(Filters.regex('^(' + bt.base['uz'][2] + ')$'), get_users),
                   MessageHandler(Filters.regex('^(' + bt.base['uz'][3] + ')$'), add_data),

                   MessageHandler(Filters.regex('^(' + bt.base['ru'][0] + ')$'), add_admin),
                   MessageHandler(Filters.regex('^(' + bt.base['ru'][1] + ')$'), get_admins),
                   MessageHandler(Filters.regex('^(' + bt.base['ru'][2] + ')$'), get_users),
                   MessageHandler(Filters.regex('^(' + bt.base['ru'][3] + ')$'), add_data),

                   MessageHandler(Filters.regex('^(' + bt.base['en'][0] + ')$'), add_admin),
                   MessageHandler(Filters.regex('^(' + bt.base['en'][1] + ')$'), get_admins),
                   MessageHandler(Filters.regex('^(' + bt.base['en'][2] + ')$'), get_users),
                   MessageHandler(Filters.regex('^(' + bt.base['en'][3] + ')$'), add_data),
                   ],
        st.ADD_ADMIN: [CommandHandler('start', start),
                       CommandHandler('admin', admin),
                       MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
                       MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
                       MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
                       MessageHandler(Filters.text, get_admin_id),
                       ],
        st.ADMINS: [CommandHandler('start', start),
                    CommandHandler('admin', admin),
                    CallbackQueryHandler(delete_admin),
                    ],
        st.ADD_DATA: [CommandHandler('start', start),
                      CommandHandler('admin', admin),
                      MessageHandler(Filters.regex('^(' + bt.back['uz'] + ')$'), admin),
                      MessageHandler(Filters.regex('^(' + bt.back['ru'] + ')$'), admin),
                      MessageHandler(Filters.regex('^(' + bt.back['en'] + ')$'), admin),
                      MessageHandler(Filters.document, get_data),
                      ],
    },
    fallbacks=[]
)

dispatcher.add_handler(all_handlers)
updater.start_polling()
updater.idle()
print('Bot is running...')
