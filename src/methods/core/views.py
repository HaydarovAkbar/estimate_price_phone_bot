from telegram import Update
from telegram.ext import CallbackContext

from states import States as st


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Salom!")
    return st.START