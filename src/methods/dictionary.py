class AdminButton:
    adm_menu = {
        'uz': ["👤 Foydalanuvchi qo'shish", "Tashkilot qo'shish", "Tashkilot o'chirish", "⚙️ Sozlamalar",
               "Foydalanuvchi o'chirish"],
        'ru': ["👤 Foydalanuvchi qo'shish", "Tashkilot qo'shish", "Tashkilot o'chirish", "⚙️ Настройки",
               "Foydalanuvchi o'chirish"],
        'en': ["👤 Foydalanuvchi qo'shish", "Tashkilot qo'shish", "Tashkilot o'chirish", "⚙️ Settings",
               "Foydalanuvchi o'chirish"]
    }
    adm_user_menu = {
        'uz': ["✳️ Aktivlashtirish", "⛔️ Tahrirlash", "⬅️ Orqaga"],
        'ru': ["✳️ Активировать", "⛔️ Редактировать", "⬅️ Назад"],
        'en': ["✳️ Activate", "⛔️ Edit", "⬅️ Back"]
    }
    adm_settings = {
        'uz': ["Tilni o'zgartirish 🌐", "⬅️ Orqaga"],
        'ru': ["Изменить язык 🌐", "⬅️ Orqaga"],
        'en': ["Change language 🌐", "⬅️ Orqaga"]
    }
    adm_roles = {
        'uz': ["Rahbar 👮‍♀️", "Kassir 👨🏻‍💻", "Rahbar va Kassir", "⬅️ Orqaga", "O'chirish 🪓"],
        'ru': ["Rahbar 👮‍♀️", "Кассир 👨🏻‍💻", "Rahbar и Кассир", "⬅️ Назад", "Удалить 🪓"],
        'en': ["Rahbar 👮‍♀️", "Cashier 👨🏻‍💻", "Rahbar and Cashier", "⬅️ Back", "Delete 🪓"]
    }

    inline_back = {
        'uz': "⬅️ Orqaga",
        'ru': "⬅️ Назад",
        'en': "⬅️ Back"
    }


class AdmTexts:
    start = {
        'uz': 'Assalom alaykum, {}!\n\nBotdan foydalanishingiz mumkin!',
        'ru': 'Здравствуйте, {}!\n\nВы можете использовать бота!',
        'en': 'Hello, {}!\n\nYou can use the bot!'
    }
    get_user = {
        'uz': '<b>Foydalanuvchi buyruqlaridan birini tanlang!</b>',
        'ru': '<b>Выберите одну из команд пользователей!</b>',
        'en': '<b>Choose one of the user commands!</b>'
    }

    settings = {
        'uz': '<b>Sozlamalar menyusidan buyruqlarni tanlang!</b>',
        'ru': '<b>Выберите одну из команд меню настроек!</b>',
        'en': '<b>Choose one of the settings menu commands!</b>'
    }

    change_language = {
        'uz': '<b>Tilni tanlang!</b>',
        'ru': '<b>Выберите язык!</b>',
        'en': '<b>Choose language!</b>'
    }

    add_user = {
        'uz': "<code>O'zgartirmoqchi bo'lgan foydalanuvchini tanlang</code>",
        'ru': "<code>Выберите пользователя, которого хотите изменить</code>",
        'en': "<code>Choose the user you want to change</code>"
    }

    user_already_exists = {
        'uz': '<code>Bu foydalanuvchi allaqachon ro\'yxatdan o\'tgan!</code>',
        'ru': '<code>Этот пользователь уже зарегистрирован!</code>',
        'en': '<code>This user is already registered!</code>'
    }

    user_added = {
        'uz': '<code>Foydalanuvchiga role ham biriktirildi!</code>',
        'ru': '<code>Пользователь добавлен в список!</code> \n\n<b>Добавленный пользователь войдет в группу</b>',
        'en': '<code>User added to the list!</code> \n\n<b>The added user will enter the group</b>'
    }

    adm_roles = {
        'uz': ["Admin 👮‍♀️", "Kassir 👨🏻‍💻", "Admin va Kassir", "⬅️ Orqaga", "O'chirish 🪓"],
        'ru': ["Админ 👮‍♀️", "Кассир 👨🏻‍💻", "Админ️ и Кассир", "⬅️ Назад", "Удалить 🪓"],
        'en': ["Admin 👮‍♀️", "Cashier 👨🏻‍💻", "Admin and Cashier", "⬅️ Back", "Delete 🪓"]
    }

    roles = {
        'uz': 'Foydalanuvchini qaysi rolga qo\'shmoqchisiz tanlang',
        'ru': 'Выберите, в какую роль добавить пользователя',
        'en': 'Choose which role to add the user'
    }

    choose_organization = {
        'uz': "<b>Foydalanuvchini qaysi tashkilotga qo'shmoqchisiz tanlang</b>",
        'ru': "<b>Выберите, в какую организацию добавить пользователя</b>",
        'en': "<b>Choose which organization to add the user</b>"
    }

    change_user = {
        'uz': "<code>{}</code> - foydalanuvchisini qaysi parametrlarini o'zgartirmoqchisiz tanlang",
        'ru': "Выберите, какие параметры пользователя {} хотите изменить",
        'en': "Choose which parameters of user {} you want to change"
    }

    add_organization = {
        'uz': "Tashkilot nomini kiriting",
        'ru': "Введите название организации",
        'en': "Enter the name of the organization"
    }
    add_organ_phone = {
        'uz': "Tashkilot telefon raqamini kiriting",
        'ru': "Введите номер телефона организации",
        'en': "Enter the phone number of the organization"
    }
    add_organ_address = {
        'uz': "Tashkilot manzilini kiriting",
        'ru': "Введите адрес организации",
        'en': "Enter the address of the organization"
    }
    add_organ_leader = {
        'uz': "Tashkilot rahbarini kiriting",
        'ru': "Введите руководителя организации",
        'en': "Enter the leader of the organization"
    }

    organization_added = {
        'uz': "<b>Tashkilot muvaffaqiyatli qo'shildi!</b>\n\n<code>Tashkilot foydalanadigan yoqilg'i turlarini tanlang 👇</code>",
        'ru': "<b>Организация успешно добавлена!</b>",
        'en': "<b>Organization added successfully!</b>"
    }
    delete_organization = {
        'uz': "O'chiriladigan tashkilotni tanlang",
        'ru': "Выберите удаляемую организацию",
        'en': "Choose the organization to be deleted"
    }
    delete_organization_success = {
        'uz': "<b>Tashkilot muvaffaqiyatli o'chirildi!</b>",
        'ru': "<b>Организация успешно удалена!</b>",
        'en': "<b>Organization successfully deleted!</b>"
    }
    add_organ_fuel_column = {
        'uz': "<b>Tashkilot yoqilg'i turlari muvafaqiyatli kiritildi</b>\n\n{} - yoqilg'i uchun ustunlarni tanlang",
        'ru': "<b>Топливо успешно введено</b>\n\n{} - выберите столбцы для топлива",
        'en': "<b>Fuel successfully entered</b>\n\n{} - choose columns for fuel"
    }
    again_enter_fuel_type = {
        'uz': "<b>Qaytadan yoqilg'i turlarini tanlang</b>",
        'ru': "<b>Выберите топливо снова</b>",
        'en': "<b>Choose fuel again</b>"
    }
    added_organization = {
        'uz': "<code>Tashkilot barcha ma'lumotlari muvaffaqiyatli kiritildi. ✅✅✅</code>",
        'ru': "<b>Все данные организации успешно введены.</b>",
        'en': "<b>All organization data entered successfully.</b>"
    }
    user_deleted = {
        'uz': "<b>Foydalanuvchi muvaffaqiyatli o'chirildi!</b>",
        'ru': "<b>Пользователь успешно удален!</b>",
        'en': "<b>User successfully deleted!</b>"
    }
    delete_user = {
        'uz': "<b>O'chiriladigan foydalanuvchini [CHAT_ID] telegram id raqamini kiriting</b>",
        'ru': "<b>Введите telegram id номер удаляемого пользователя</b>",
        'en': "<b>Enter the telegram id number of the user to be deleted</b>"
    }
    wrong_id = {
        'uz': "<b>Telegram id raqam noto'g'ri kiritildi yoki bunday foydalanuvchi topilmadi! \n\nQaytadan urinib ko'ring</b>",
        'ru': "<b>Неверно введен номер telegram id или такой пользователь не найден! Попробуйте еще раз</b>",
        'en': "<b>Telegram id number entered incorrectly or such user not found! Try again</b>"
    }


class Button:
    adm_menu = {
        'uz': ["👤 Foydalanuvchi boshqaruvi", "Tashkilot qo'shish", "⚙️ Sozlamalar"],
        'ru': ["👤 Управление Пользователями", "Tashkilot qo'shish", "⚙️ Настройки"],
        'en': ["👤 User Management", "Tashkilot qo'shish", "⚙️ Settings"]
    }
    adm_user_menu = {
        'uz': ["✳️ Aktivlashtirish", "⛔️ Tahrirlash", "⬅️ Orqaga"],
        'ru': ["✳️ Активировать", "⛔️ Редактировать", "⬅️ Назад"],
        'en': ["✳️ Activate", "⛔️ Edit", "⬅️ Back"]
    }
    adm_settings = {
        'uz': ["Tilni o'zgartirish 🌐", "⬅️ Orqaga"],
        'ru': ["Изменить язык 🌐", "⬅️ Orqaga"],
        'en': ["Change language 🌐", "⬅️ Orqaga"]
    }
    adm_roles = {
        'uz': ["Admin 👮‍♀️", "Kassir 👨🏻‍💻", "Admin va Kassir", "⬅️ Orqaga", "O'chirish 🪓"],
        'ru': ["Админ 👮‍♀️", "Кассир 👨🏻‍💻", "Админ️ и Кассир", "⬅️ Назад", "Удалить 🪓"],
        'en': ["Admin 👮‍♀️", "Cashier 👨🏻‍💻", "Admin and Cashier", "⬅️ Back", "Delete 🪓"]
    }

    inline_back = {
        'uz': "⬅️ Orqaga",
        'ru': "⬅️ Назад",
        'en': "⬅️ Back"
    }


# class AdmTexts:
#     start = {
#         'uz': 'Assalom alaykum, {}!\n\nBotdan foydalanishingiz mumkin!',
#         'ru': 'Здравствуйте, {}!\n\nВы можете использовать бота!',
#         'en': 'Hello, {}!\n\nYou can use the bot!'
#     }
#     get_user = {
#         'uz': '<b>Foydalanuvchi buyruqlaridan birini tanlang!</b>',
#         'ru': '<b>Выберите одну из команд пользователей!</b>',
#         'en': '<b>Choose one of the user commands!</b>'
#     }
#
#     settings = {
#         'uz': '<b>Sozlamalar menyusidan buyruqlarni tanlang!</b>',
#         'ru': '<b>Выберите одну из команд меню настроек!</b>',
#         'en': '<b>Choose one of the settings menu commands!</b>'
#     }
#
#     change_language = {
#         'uz': '<b>Tilni tanlang!</b>',
#         'ru': '<b>Выберите язык!</b>',
#         'en': '<b>Choose language!</b>'
#     }
#
#     add_user = {
#         'uz': "<code>O'zgartirmoqchi bo'lgan foydalanuvchini tanlang</code>",
#         'ru': "<code>Выберите пользователя, которого хотите изменить</code>",
#         'en': "<code>Choose the user you want to change</code>"
#     }
#
#     user_already_exists = {
#         'uz': '<code>Bu foydalanuvchi allaqachon ro\'yxatdan o\'tgan!</code>',
#         'ru': '<code>Этот пользователь уже зарегистрирован!</code>',
#         'en': '<code>This user is already registered!</code>'
#     }
#
#     user_added = {
#         'uz': '<code>Foydalanuvchi ro\'yxatga qo\'shildi!</code>\n\n<b>Qo\'shilgan foydalanuvchi guruhga kiradi</b>',
#         'ru': '<code>Пользователь добавлен в список!</code> \n\n<b>Добавленный пользователь войдет в группу</b>',
#         'en': '<code>User added to the list!</code> \n\n<b>The added user will enter the group</b>'
#     }
#
#     adm_roles = {
#         'uz': ["Admin 👮‍♀️", "Kassir 👨🏻‍💻", "Admin va Kassir", "⬅️ Orqaga", "O'chirish 🪓"],
#         'ru': ["Админ 👮‍♀️", "Кассир 👨🏻‍💻", "Админ️ и Кассир", "⬅️ Назад", "Удалить 🪓"],
#         'en': ["Admin 👮‍♀️", "Cashier 👨🏻‍💻", "Admin and Cashier", "⬅️ Back", "Delete 🪓"]
#     }
#
#     roles = {
#         'uz': 'Foydalanuvchini qaysi rolga qo\'shmoqchisiz tanlang',
#         'ru': 'Выберите, в какую роль добавить пользователя',
#         'en': 'Choose which role to add the user'
#     }
#
#     change_user = {
#         'uz': "{} - foydalanuvchisini qaysi parametrlarini o'zgartirmoqchisiz tanlang",
#         'ru': "Выберите, какие параметры пользователя {} хотите изменить",
#         'en': "Choose which parameters of user {} you want to change"
#     }


class KButtons:
    menu = {
        'uz': ["🔢 Kalonka ko'rsatkichi", "💰 Bugungi savdo", "Bugungi narxlar 💵", "⚙️ Sozlamalar"],
        'ru': ["🔢 Указатель колонки", "💰 Сегодняшняя продажа", "Сегодняшние цены 💵", "⚙️ Настройки"],
        'en': ["🔢 Column pointer", "💰 Today's sale", "Today's prices 💵", "⚙️ Settings"]
    }

    fuel_columns = {
        'uz': ["🕑 Kun boshiga", "Kun oxiriga 🕘", "⬅️ Orqaga"],
        'ru': ["🕑 На начало дня", "На конец дня 🕘", "⬅️ Назад"],
        'en': ["🕑 At the beginning of the day", "At the end of the day 🕘", "⬅️ Back"]
    }
    k_settings = {
        'uz': ["Tilni o'zgartirish 🌐", "⬅️ Orqaga"],
        'ru': ["Изменить язык 🌐", "⬅️ Orqaga"],
        'en': ["Change language 🌐", "⬅️ Orqaga"]
    }


class KTexts:
    start = {
        'uz': 'Assalom alaykum, {}!\n\nBotdan foydalanishingiz mumkin!',
        'ru': 'Здравствуйте, {}!\n\nВы можете использовать бота!',
        'en': 'Hello, {}!\n\nYou can use the bot!'
    }
    fuel_column = {
        'uz': "<b>Qaysi kalonka ko'rsatgichini tanlamoqchisiz?</b>",
        'ru': "<b>Какой колонки вы хотите выбрать?</b>",
        'en': "<b>Which fuel column do you want to choose?</b>"
    }
    column_chosen = {
        'uz': "<b>Siz <code>{}</code> yoqilg'i uchun <code> {} </code> kalonkasini tanladingiz!\n\nKalonka ko'rsatgichini qaysi vaqt uchun kiritmoqchisiz tanlang va kiriting</b>",
        'ru': "<b>Вы выбрали колонку <code> {} </code> для топлива <code>{}</code>!\n\nВыберите и введите время для колонки</b>",
        'en': "<b>You have chosen column <code> {} </code> for fuel <code>{}</code>!\n\nChoose and enter the time for the column</b>"
    }
    fuel_column_numbers = {
        'uz': "Kalonka ko'rsatgichini kiriting",
        'ru': "Введите номер колонки",
        'en': "Enter the column number"
    }

    fuel_type = {
        'uz': "<b>Qaysi turdagi yoqilg'i uchun kiritmoqchisiz tanlang</b>",
        'ru': "<b>Выберите, для какого типа топлива вы хотите ввести данные</b>",
        'en': "<b>Choose for which type of fuel you want to enter data</b>"
    }

    fuel_type_chosen = {
        'uz': "<b>Siz <code> {} </code> turdagi yoqilg'i uchun tanladingiz!</b>",
        'ru': "<b>Вы выбрали топливо для типа <code> {} </code>!</b>",
        'en': "<b>You have chosen fuel for the type <code> {} </code>!</b>"
    }
    column_num_already_exist_1 = {
        'uz': "<b>Bu vaqt uchun bu raqamli kalonka allaqachon kiritilgan!\n\nKun boshidagi ko'rsatgich: {}</b>",
        'ru': "<b>Этот номер колонки уже введен для этого времени!\n\nКолонка на начало дня: {}</b>",
        'en': "<b>This column number has already been entered for this time!\n\nColumn at the beginning of the day: {}</b>"
    }
    column_num_already_exist_2 = {
        'uz': "<b>Bu vaqt uchun bu raqamli kalonka allaqachon kiritilgan!\n\nKun oxiridagi ko'rsatgich: {}</b>",
        'ru': "<b>Этот номер колонки уже введен для этого времени!\n\nКолонка на конец дня: {}</b>",
        'en': "<b>This column number has already been entered for this time!\n\nColumn at the end of the day: {}</b>"
    }
    column_num_success = {
        'uz': "<b>Kalonka raqami muvaffaqiyatli kiritildi!</b>",
        'ru': "<b>Номер колонки успешно введен!</b>",
        'en': "<b>Column number entered successfully!</b>"
    }

    column_num_error = {
        'uz': "<b>Kalonka raqami raqam bo'lishi kerak!</b>",
        'ru': "<b>Номер колонки должен быть числом!</b>",
        'en': "<b>Column number must be a number!</b>"
    }
    column_num_add_first = {
        'uz': "<b>Avvalo kun boshidagi ko'rsatgichlarni kiritishingiz kerak bo'ladi!</b>",
        'ru': "<b>Сначала нужно ввести колонки на начало дня!</b>",
        'en': "<b>First you need to enter columns at the beginning of the day!</b>"
    }

    column_pointer_already_exist = {
        'uz': "<b>Bu vaqt uchun bu raqamli ko'rsatgich allaqachon kiritilgan!\n\nKun boshida: {}\nKun oxirida: {}</b>",
        'ru': "<b>Этот номер указателя уже введен для этого времени!\n\nНа начало дня: {}\nНа конец дня: {}</b>",
        'en': "<b>This column number has already been entered for this time!\n\nAt the beginning of the day: {}\nAt the end of the day: {}</b>"
    }

    fuel_size_input = {
        'uz': "<b>Yoqilg'i hajmini kiriting</b>",
        'ru': "<b>Введите объем топлива</b>",
        'en': "<b>Enter the fuel volume</b>"
    }

    fuel_size_error = {
        'uz': "<b>Yoqilg'i hajmi raqam bo'lishi kerak! \n\nQaytadan urinib ko'ring</b>",
        'ru': "<b>Объем топлива должен быть числом! \n\nПопробуйте еще раз</b>",
        'en': "<b>Fuel volume must be a number! \n\nTry again</b>"
    }
    fuel_size_added_success = {
        'uz': "<b>Yoqilg'i hajmi muvaffaqiyatli kiritildi!</b>",
        'ru': "<b>Объем топлива успешно введен!</b>",
        'en': "<b>Fuel volume entered successfully!</b>"
    }

    fuel_already_added = {
        'uz': "<b>Bu vaqt uchun bu turdagi yoqilg'i allaqachon kiritilgan!</b>",
        'ru': "<b>Этот тип топлива уже введен для этого времени!</b>",
        'en': "<b>This type of fuel has already been entered for this time!</b>"
    }
    choose_payment_type = {
        'uz': "<b>Qaysi to'lov turida savdo hajmini kiritmoqchisiz tanlang</b>",
        'ru': "<b>Выберите тип оплаты, для которого хотите ввести объем продажи</b>",
        'en': "<b>Choose the type of payment for which you want to enter the sales volume</b>"
    }
    input_fuel_price = {
        'uz': "<b>Bugungi yoqilg'ining sotilgan narxini kiriting!</b>",
        'ru': "<b>Введите цену проданного топлива сегодня!</b>",
        'en': "<b>Enter the price of the fuel sold today!</b>"
    }
    fuel_price_added_success = {
        'uz': "<b>Yoqilg'ining sotilgan narxi muvaffaqiyatli kiritildi!</b>",
        'ru': "<b>Цена проданного топлива успешно введена!</b>",
        'en': "<b>The price of the fuel sold was entered successfully!</b>"
    }
    fuel_price_error = {
        'uz': "<b>Yoqilg'ining sotilgan narxi raqam bo'lishi kerak! \n\nQaytadan urinib ko'ring</b>",
        'ru': "<b>Цена проданного топлива должна быть числом! \n\nПопробуйте еще раз</b>",
        'en': "<b>The price of the fuel sold must be a number! \n\nTry again</b>"
    }
    get_user = {
        'uz': '<b>Foydalanuvchi buyruqlaridan birini tanlang!</b>',
        'ru': '<b>Выберите одну из команд пользователей!</b>',
        'en': '<b>Choose one of the user commands!</b>'
    }
    change_language = {
        'uz': "<b>Tilni tanlang!</b>",
        'ru': "<b>Выберите язык!</b>",
        'en': "<b>Choose language!</b>"
    }
    fuel_price_already_added = {
        'uz': "<b>Bu vaqt uchun bu turdagi yoqilg'i narxi allaqachon kiritilgan!</b>",
        'ru': "<b>Цена проданного топлива этого типа уже введена для этого времени!</b>",
        'en': "<b>The price of the fuel sold of this type has already been entered for this time!</b>"
    }


class LeaderTexts:
    start = {
        'uz': 'Assalom alaykum, {}!\n\nBotdan foydalanishingiz mumkin!',
        'ru': 'Здравствуйте, {}!\n\nВы можете использовать бота!',
        'en': 'Hello, {}!\n\nYou can use the bot!'
    }

    input_fuel_type = {
        'uz': "<b>Qaysi turdagi yoqilg'i uchun kiritmoqchisiz tanlang</b>",
        'ru': "<b>Выберите, для какого типа топлива вы хотите ввести данные</b>",
        'en': "<b>Choose for which type of fuel you want to enter data</b>"
    }
    fuel_size_input = {
        'uz': "<b>Yoqilg'i hajmini kiriting</b>",
        'ru': "<b>Введите объем топлива</b>",
        'en': "<b>Enter the fuel volume</b>"
    }


class LeaderKeyboardText:
    menu = {
        'uz': ["📥 Yoqilg'i kirim qilish", "Hisobot olish 📤", "⚙️ Sozlamalar"],
        'ru': ["📥 Ввод топлива", "Получить отчет 📤", "⚙️ Настройки"],
        'en': ["📥 Fuel input", "Get report 📤", "⚙️ Settings"]
    }
