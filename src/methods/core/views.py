from telegram import Update
from telegram.ext import CallbackContext

from .texts import Message as msg_txt
from .keyboards import KeyboardBase as kb

from db.models import User, Channels

from states import States as st


async def start(update: Update, context: CallbackContext):
    user, _ = User.objects.get_or_create(chat_id=update.effective_user.id,
                                         defaults={'fullname': update.effective_user.full_name,
                                                   'username': update.effective_user.username})
    channels = Channels.objects.filter(is_active=True)
    if channels.exists():
        i = int()
        for channel in channels:
            is_followers = await context.bot.get_chat_member(channel.chat_id, user.chat_id)
            if is_followers.status in ['member', 'administrator']:
                i += 1
        if i == channels.count():
            await update.message.reply_text()
            return st.MAIN_MENU
    else:
        await update.message.reply_text(f"Salom, {user.fullname}!\n"
                                        f"Quyidagi tugmalardan birini tanlang:")
        return st.MAIN_MENU