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
from states import States as st
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, Filters, \
    CallbackQueryHandler, Updater

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

all_handlers = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        st.START: [CommandHandler('start', start)],
        st.FOLLOWERS: [CommandHandler('start', start),
                       CallbackQueryHandler(followers)],
    },
    fallbacks=[]
)

dispatcher.add_handler(all_handlers)
updater.start_polling()
updater.idle()
print('Bot is running...')
