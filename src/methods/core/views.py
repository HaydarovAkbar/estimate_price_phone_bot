from telegram import Update
from telegram.ext import CallbackContext

from .texts import Message as msg_txt
from .keyboards import KeyboardBase as kb

from db.models import User, Channels

from states import States as st


async def start(update: Update, context: CallbackContext):
    user, _ = User.objects.get_or_create(chat_id=update.effective_user.id,
                                         defaults={'fullname': update.effective_user.full_name,
                                                   'username': update.effective_user.username,
                                                   'language': 'uz', })
    channels = Channels.objects.filter(is_active=True)
    if channels.exists():
        i = int()
        locout_ch = list()
        for channel in channels:
            is_followers = await context.bot.get_chat_member(channel.chat_id, user.chat_id)
            if is_followers.status in ['member', 'administrator']:
                i += 1
            else:
                locout_ch.append(channel)
        if i == channels.count():
            await update.message.reply_text(msg_txt.main.get(user.language),
                                            reply_markup=kb.get_main_menu(user.language))
            return st.MAIN_MENU
        else:
            await update.message.reply_text(msg_txt.forced_labor.get(user.language),
                                            reply_markup=kb.channels(locout_ch))
            return st.FOLLOWERS
    else:
        await update.message.reply_text(msg_txt.main.get(user.language),
                                        reply_markup=kb.get_main_menu(user.language))
        return st.MAIN_MENU
