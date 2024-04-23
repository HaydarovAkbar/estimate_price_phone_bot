class MessageText:
    main = {
        'uz': "Admin panelga xush kelibsiz, {}!",
        'ru': "Добро пожаловать в админ панель, {}!",
        'en': "Welcome to the admin panel, {}!",
    }

    add_admin = {
        'uz': "Yangi admin qo'shish uchun foydalanuvchi CHAT ID sini kiriting",
        'ru': "Введите CHAT ID пользователя для добавления нового админа",
        'en': "Enter the CHAT ID of the user to add a new admin",
    }

    error_id = {
        'uz': "CHAT ID raqamini kiriting",
        'ru': "Введите номер CHAT ID",
        'en': "Enter the CHAT ID number",
    }
    success = {
        'uz': "Muvaffaqiyatli bajarildi ✅",
        'ru': "успешно добавлен в админы ✅",
        'en': "successfully added to admins ✅",
    }
    already_admin = {
        'uz': "Bu foydalanuvchi allaqachon admin",
        'ru': "Этот пользователь уже админ",
        'en': "This user is already an admin",
    }

    admins = {
        'uz': "Adminlar ro'yxati \n\n",
        'ru': "Список админов \n\n",
        'en': "List of admins \n\n",
    }
    no_admins = {
        'uz': "Hozircha adminlar yo'q",
        'ru': "Пока нет админов",
        'en': "No admins yet",
    }
    delete_admin = {
        'uz': "\n\n🪓 Barcha adminlar ro'yxati - O'chirish uchun tanlang",
        'ru': "\n\n🪓 Список всех админов - Выберите для удаления",
        'en': "\n\n🪓 List of all admins - Select to delete",
    }

    add_data = {
        'uz': "Berilgan shabllonni to'ldirib yuboring!",
        'ru': "Заполните предоставленный шаблон!",
        'en': "Fill in the provided template!",
    }

    add_channel = {
        'uz': "Kanal nomini kiriting",
        'ru': "Введите название канала",
        'en': "Enter the channel name",
    }

    add_channel_url = {
        'uz': "Kanal linkini kiriting",
        'ru': "Введите ссылку на канал",
        'en': "Enter the channel link",
    }

    add_channel_id = {
        'uz': "Kanal ID sini kiriting",
        'ru': "Введите ID канала",
        'en': "Enter the channel ID",
    }

    channel_added = {
        'uz': "Kanal muvaffaqiyatli qo'shildi \n\nEslatma!!! Kanalni aktivlashtirish uchun botni kanalga admin qilish zarur",
        'ru': "Канал успешно добавлен \n\nВнимание!!! Для активации канала необходимо назначить бота админом в канале",
        'en': "Channel successfully added \n\nAttention!!! To activate the channel, you need to make the bot an admin in the channel",
    }

    channel_deleted = {
        'uz': "Kanal muvaffaqiyatli o'chirildi",
        'ru': "Канал успешно удален",
        'en': "Channel successfully deleted",
    }

    channel_already_exists = {
        'uz': "Bu kanal allaqachon mavjud",
        'ru': "Этот канал уже существует",
        'en': "This channel already exists",
    }

    channels = {
        'uz': "Kanallar ro'yxati: \n🪓 Kanalni o'chirish uchun tanlang",
        'ru': "Список каналов: \n🪓 Выберите для удаления канала",
        'en': "List of channels: \n🪓 Select to delete the channel",
    }

    no_channels = {
        'uz': "Hozircha kanallar yo'q",
        'ru': "Пока нет каналов",
        'en': "No channels yet",
    }

    error_channel = {
        'uz': "Kanal topilmadi",
        'ru': "Канал не найден",
        'en': "Channel not found",
    }

    fill_template = {
        'uz': "Reklama xabarini yuboring",
        'ru': "Отправьте рекламное сообщение",
        'en': "Send an ad message",
    }


class KeyboardsAdmin:
    base = {
        'uz': ["Admin qo'shish", "Adminlar", "Foydalanuvchilar", "Ma'lumot qo'shish", "Kanal qo'shish",
               "Kanalni o'chirish", "Reklama yuborish"],
        'ru': ["Добавить админа", "Админы", "Пользователи", "Добавить данные", "Добавить канал", "Удалить канал",
               "Отправить рекламу"],
        'en': ["Add admin", "Admins", "Users", "Add data", "Add channel", "Delete channel", "Send ad"],
    }
    back = {
        'uz': '🔙 Orqaga',
        'ru': '🔙 Назад',
        'en': '🔙 Back',
    }
