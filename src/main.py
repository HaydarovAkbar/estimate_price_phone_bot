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

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from methods.core.views import start
from states import States as st

app = ApplicationBuilder().token(TOKEN).build()

all_handlers = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        st.START: [CommandHandler('start', start),
                   MessageHandler(filters.TEXT, start)],
    },
    fallbacks=[]
)

app.add_handler(all_handlers)

app.run_polling()
print("run polling")
