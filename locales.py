TEXTS: dict[str, dict[str, str]] = {

    # ── Til tanlash ──────────────────────────────────────────────
    "choose_language": {
        "uz": "🌐 <b>Tilni tanlang:</b>",
        "ru": "🌐 <b>Выберите язык:</b>",
        "en": "🌐 <b>Choose your language:</b>",
    },
    "language_set": {
        "uz": "✅ Til o'rnatildi: O'zbekcha",
        "ru": "✅ Язык установлен: Русский",
        "en": "✅ Language set: English",
    },

    # ── Asosiy menyu ─────────────────────────────────────────────
    "welcome": {
        "uz": (
            "📚 <b>Kutubxona</b>\n\n"
            "Quyidagi kategoriyalardan birini tanlang yoki "
            "pastdagi menyudan foydalaning."
        ),
        "ru": (
            "📚 <b>Библиотека</b>\n\n"
            "Выберите одну из категорий или воспользуйтесь меню внизу."
        ),
        "en": (
            "📚 <b>Library</b>\n\n"
            "Choose a category below or use the bottom menu."
        ),
    },

    # ── Reply keyboard tugmalari ──────────────────────────────────
    "btn_settings_reply": {
        "uz": "⚙️ Sozlamalar",
        "ru": "⚙️ Настройки",
        "en": "⚙️ Settings",
    },
    "btn_admin_reply": {
        "uz": "👨‍💼 Admin",
        "ru": "👨‍💼 Admin",
        "en": "👨‍💼 Admin",
    },

    # ── Obuna ────────────────────────────────────────────────────
    "not_subscribed": {
        "uz": (
            "⚠️ <b>Botdan foydalanish uchun\n"
            "quyidagi kanallarga obuna bo'ling:</b>"
        ),
        "ru": (
            "⚠️ <b>Для использования бота\n"
            "подпишитесь на каналы:</b>"
        ),
        "en": (
            "⚠️ <b>To use the bot,\n"
            "subscribe to the channels:</b>"
        ),
    },
    "btn_check_sub": {
        "uz": "✅ Tekshirish",
        "ru": "✅ Проверить",
        "en": "✅ Check",
    },
    "sub_ok": {
        "uz": "✅ Obuna tasdiqlandi!",
        "ru": "✅ Подписка подтверждена!",
        "en": "✅ Subscription confirmed!",
    },
    "sub_fail": {
        "uz": "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!",
        "ru": "❌ Вы ещё не подписались на все каналы!",
        "en": "❌ You haven't subscribed to all channels yet!",
    },

    # ── Kategoriyalar ─────────────────────────────────────────────
    "no_categories": {
        "uz": "😔 Hozircha kategoriyalar mavjud emas.",
        "ru": "😔 Пока нет категорий.",
        "en": "😔 No categories available yet.",
    },
    "choose_file": {
        "uz": "📄 Faylni tanlang:",
        "ru": "📄 Выберите файл:",
        "en": "📄 Choose a file:",
    },

    # ── Fayllar ───────────────────────────────────────────────────
    "no_files": {
        "uz": "😔 Bu kategoriyada hozircha fayllar yo'q.",
        "ru": "😔 В этой категории пока нет файлов.",
        "en": "😔 No files in this category yet.",
    },
    "downloading": {
        "uz": "⬇️ Fayl yuborilmoqda...",
        "ru": "⬇️ Отправка файла...",
        "en": "⬇️ Sending file...",
    },
    "file_caption": {
        "uz": "📥 <b>{name}</b>\n📂 {category}\n⬇️ Yuklab olindi: <b>{count}</b> marta",
        "ru": "📥 <b>{name}</b>\n📂 {category}\n⬇️ Скачано: <b>{count}</b> раз",
        "en": "📥 <b>{name}</b>\n📂 {category}\n⬇️ Downloaded: <b>{count}</b> times",
    },
    "btn_back_cats": {
        "uz": "⬅️ Kategoriyalar",
        "ru": "⬅️ Категории",
        "en": "⬅️ Categories",
    },

    # ── Sozlamalar ────────────────────────────────────────────────
    "settings_title": {
        "uz": "⚙️ <b>Sozlamalar</b>\n\n🌐 Joriy til: <b>{lang_name}</b>",
        "ru": "⚙️ <b>Настройки</b>\n\n🌐 Текущий язык: <b>{lang_name}</b>",
        "en": "⚙️ <b>Settings</b>\n\n🌐 Current language: <b>{lang_name}</b>",
    },
    "btn_change_lang": {
        "uz": "🌐 Tilni o'zgartirish",
        "ru": "🌐 Изменить язык",
        "en": "🌐 Change language",
    },
    "btn_close": {
        "uz": "❌ Yopish",
        "ru": "❌ Закрыть",
        "en": "❌ Close",
    },

    # ── Admin — kirish ────────────────────────────────────────────
    "admin_enter_password": {
        "uz": "🔐 <b>Admin paneli</b>\n\nParolni kiriting:",
        "ru": "🔐 <b>Панель администратора</b>\n\nВведите пароль:",
        "en": "🔐 <b>Admin Panel</b>\n\nEnter the password:",
    },
    "admin_wrong_password": {
        "uz": "❌ Noto'g'ri parol!\n<i>Qolgan urinish: {left}</i>",
        "ru": "❌ Неверный пароль!\n<i>Осталось попыток: {left}</i>",
        "en": "❌ Wrong password!\n<i>Attempts left: {left}</i>",
    },
    "admin_locked": {
        "uz": "🔒 Juda ko'p noto'g'ri urinish. Keyinroq urinib ko'ring.",
        "ru": "🔒 Слишком много попыток. Попробуйте позже.",
        "en": "🔒 Too many attempts. Try again later.",
    },
    "admin_logout_done": {
        "uz": "✅ Admin paneldan chiqdingiz.",
        "ru": "✅ Вы вышли из панели администратора.",
        "en": "✅ Logged out of admin panel.",
    },

    # ── Admin — panel ─────────────────────────────────────────────
    "admin_panel": {
        "uz": (
            "⚙️ <b>Admin Panel</b>\n\n"
            "Kategoriyalar, fayllar va kanallarni boshqaring."
        ),
        "ru": (
            "⚙️ <b>Панель администратора</b>\n\n"
            "Управляйте категориями, файлами и каналами."
        ),
        "en": (
            "⚙️ <b>Admin Panel</b>\n\n"
            "Manage categories, files and channels."
        ),
    },
    "btn_add_category": {"uz": "➕ Kategoriya qo'sh", "ru": "➕ Добавить категорию", "en": "➕ Add category"},
    "btn_del_category": {"uz": "🗑 Kategoriya o'chir", "ru": "🗑 Удалить категорию", "en": "🗑 Delete category"},
    "btn_add_file":     {"uz": "📤 Fayl qo'sh",        "ru": "📤 Добавить файл",     "en": "📤 Add file"},
    "btn_del_file":     {"uz": "🗑 Fayl o'chir",        "ru": "🗑 Удалить файл",      "en": "🗑 Delete file"},
    "btn_channels":     {"uz": "📢 Kanallar",           "ru": "📢 Каналы",            "en": "📢 Channels"},
    "btn_stats":        {"uz": "📊 Statistika",         "ru": "📊 Статистика",        "en": "📊 Statistics"},
    "btn_change_pwd":   {"uz": "🔑 Parol o'zgart.",     "ru": "🔑 Изм. пароль",      "en": "🔑 Change pwd"},
    "btn_logout":       {"uz": "🚪 Chiqish",            "ru": "🚪 Выйти",             "en": "🚪 Logout"},
    "btn_cancel":       {"uz": "❌ Bekor qilish",       "ru": "❌ Отмена",            "en": "❌ Cancel"},
    "btn_back_admin":   {"uz": "⬅️ Admin panel",        "ru": "⬅️ Панель адм.",      "en": "⬅️ Admin panel"},

    # ── Admin — kategoriya ────────────────────────────────────────
    "ask_cat_name_uz": {
        "uz": "📝 Kategoriya nomini <b>O'ZBEKCHA</b> kiriting:\n\n<i>(Bekor qilish uchun /cancel)</i>",
        "ru": "📝 Введите название категории на <b>УЗБЕКСКОМ</b>:\n\n<i>(Отмена: /cancel)</i>",
        "en": "📝 Enter category name in <b>UZBEK</b>:\n\n<i>(Cancel: /cancel)</i>",
    },
    "ask_cat_name_ru": {
        "uz": "📝 Kategoriya nomini <b>RUSCHA</b> kiriting:",
        "ru": "📝 Введите название категории на <b>РУССКОМ</b>:",
        "en": "📝 Enter category name in <b>RUSSIAN</b>:",
    },
    "ask_cat_name_en": {
        "uz": "📝 Kategoriya nomini <b>INGLIZCHA</b> kiriting:",
        "ru": "📝 Введите название категории на <b>АНГЛИЙСКОМ</b>:",
        "en": "📝 Enter category name in <b>ENGLISH</b>:",
    },
    "category_added": {
        "uz": "✅ Kategoriya qo'shildi!",
        "ru": "✅ Категория добавлена!",
        "en": "✅ Category added!",
    },
    "select_category_to_delete": {
        "uz": "🗑 <b>O'chiriladigan kategoriyani tanlang:</b>",
        "ru": "🗑 <b>Выберите категорию для удаления:</b>",
        "en": "🗑 <b>Select category to delete:</b>",
    },
    "category_deleted": {
        "uz": "✅ Kategoriya va uning barcha fayllari o'chirildi!",
        "ru": "✅ Категория и все её файлы удалены!",
        "en": "✅ Category and all its files deleted!",
    },

    # ── Admin — fayl ──────────────────────────────────────────────
    "ask_file_category": {
        "uz": "📂 <b>Qaysi kategoriyaga fayl qo'shilsin?</b>",
        "ru": "📂 <b>В какую категорию добавить файл?</b>",
        "en": "📂 <b>Which category to add file to?</b>",
    },
    "ask_file_name_uz": {
        "uz": "📝 Fayl nomini <b>O'ZBEKCHA</b> kiriting:\n\n<i>(Bekor qilish uchun /cancel)</i>",
        "ru": "📝 Введите название файла на <b>УЗБЕКСКОМ</b>:\n\n<i>(Отмена: /cancel)</i>",
        "en": "📝 Enter file name in <b>UZBEK</b>:\n\n<i>(Cancel: /cancel)</i>",
    },
    "ask_file_name_ru": {
        "uz": "📝 Fayl nomini <b>RUSCHA</b> kiriting:",
        "ru": "📝 Введите название файла на <b>РУССКОМ</b>:",
        "en": "📝 Enter file name in <b>RUSSIAN</b>:",
    },
    "ask_file_name_en": {
        "uz": "📝 Fayl nomini <b>INGLIZCHA</b> kiriting:",
        "ru": "📝 Введите название файла на <b>АНГЛИЙСКОМ</b>:",
        "en": "📝 Enter file name in <b>ENGLISH</b>:",
    },
    "ask_upload_file": {
        "uz": "📤 Faylni yuboring:\n<i>Qabul qilinadigan: PDF, RAR, ZIP</i>",
        "ru": "📤 Отправьте файл:\n<i>Принимаемые: PDF, RAR, ZIP</i>",
        "en": "📤 Send the file:\n<i>Accepted: PDF, RAR, ZIP</i>",
    },
    "wrong_file_type": {
        "uz": "⚠️ Faqat <b>PDF</b>, <b>RAR</b> yoki <b>ZIP</b> fayl yuboring:",
        "ru": "⚠️ Отправьте только файл <b>PDF</b>, <b>RAR</b> или <b>ZIP</b>:",
        "en": "⚠️ Please send only <b>PDF</b>, <b>RAR</b> or <b>ZIP</b> file:",
    },
    "file_added": {
        "uz": "✅ Fayl qo'shildi!",
        "ru": "✅ Файл добавлен!",
        "en": "✅ File added!",
    },
    "select_file_to_delete": {
        "uz": "🗑 <b>O'chiriladigan faylni tanlang:</b>",
        "ru": "🗑 <b>Выберите файл для удаления:</b>",
        "en": "🗑 <b>Select file to delete:</b>",
    },
    "select_cat_for_del_file": {
        "uz": "📂 <b>Qaysi kategoriyadan fayl o'chirilsin?</b>",
        "ru": "📂 <b>Из какой категории удалить файл?</b>",
        "en": "📂 <b>Which category to delete file from?</b>",
    },
    "file_deleted": {
        "uz": "✅ Fayl o'chirildi!",
        "ru": "✅ Файл удалён!",
        "en": "✅ File deleted!",
    },

    # ── Admin — kanallar ──────────────────────────────────────────
    "channels_list": {
        "uz": "📢 <b>Majburiy kanallar</b>\n\n{list}\n\nKanal qo'shish uchun «➕ Kanal qo'sh» tugmasini bosing.",
        "ru": "📢 <b>Обязательные каналы</b>\n\n{list}\n\nДля добавления нажмите «➕ Добавить канал».",
        "en": "📢 <b>Required Channels</b>\n\n{list}\n\nPress «➕ Add channel» to add one.",
    },
    "no_channels_yet": {
        "uz": "Hozircha kanallar yo'q.",
        "ru": "Каналов пока нет.",
        "en": "No channels yet.",
    },
    "btn_add_channel": {"uz": "➕ Kanal qo'sh", "ru": "➕ Добавить канал", "en": "➕ Add channel"},
    "btn_del_channel": {"uz": "🗑 Kanal o'chir", "ru": "🗑 Удалить канал", "en": "🗑 Delete channel"},
    "ask_channel_id": {
        "uz": (
            "📢 <b>Kanal ID sini kiriting</b>\n\n"
            "Misol: <code>@mening_kanalim</code> yoki <code>-1001234567890</code>\n\n"
            "<i>Bot kanalning admini bo'lishi kerak!</i>"
        ),
        "ru": (
            "📢 <b>Введите ID канала</b>\n\n"
            "Пример: <code>@my_channel</code> или <code>-1001234567890</code>\n\n"
            "<i>Бот должен быть администратором канала!</i>"
        ),
        "en": (
            "📢 <b>Enter Channel ID</b>\n\n"
            "Example: <code>@my_channel</code> or <code>-1001234567890</code>\n\n"
            "<i>Bot must be admin of the channel!</i>"
        ),
    },
    "ask_channel_title": {
        "uz": "✏️ Kanal uchun <b>nom</b> kiriting (tugmada ko'rinadi):",
        "ru": "✏️ Введите <b>название</b> канала (будет на кнопке):",
        "en": "✏️ Enter channel <b>title</b> (shown on button):",
    },
    "ask_channel_url": {
        "uz": "🔗 Kanal <b>havolasini</b> kiriting:\nMisol: <code>https://t.me/kanal_nomi</code>",
        "ru": "🔗 Введите <b>ссылку</b> на канал:\nПример: <code>https://t.me/имя_канала</code>",
        "en": "🔗 Enter channel <b>link</b>:\nExample: <code>https://t.me/channel_name</code>",
    },
    "channel_added": {
        "uz": "✅ Kanal qo'shildi!",
        "ru": "✅ Канал добавлен!",
        "en": "✅ Channel added!",
    },
    "channel_not_accessible": {
        "uz": "⚠️ Bot bu kanalga kira olmadi. Bot kanalning admini ekanligini tekshiring va qayta urinib ko'ring:",
        "ru": "⚠️ Бот не может получить доступ к каналу. Убедитесь, что бот является администратором канала, и попробуйте снова:",
        "en": "⚠️ Bot can't access this channel. Make sure bot is admin of the channel and try again:",
    },
    "select_channel_to_delete": {
        "uz": "🗑 <b>O'chiriladigan kanalni tanlang:</b>",
        "ru": "🗑 <b>Выберите канал для удаления:</b>",
        "en": "🗑 <b>Select channel to delete:</b>",
    },
    "channel_deleted": {
        "uz": "✅ Kanal o'chirildi!",
        "ru": "✅ Канал удалён!",
        "en": "✅ Channel deleted!",
    },

    # ── Admin — parol ─────────────────────────────────────────────
    "ask_new_password": {
        "uz": "🔑 Yangi parolni kiriting <b>(kamida 6 belgi)</b>:\n\n<i>Bekor qilish: /cancel</i>",
        "ru": "🔑 Введите новый пароль <b>(минимум 6 символов)</b>:\n\n<i>Отмена: /cancel</i>",
        "en": "🔑 Enter new password <b>(at least 6 characters)</b>:\n\n<i>Cancel: /cancel</i>",
    },
    "ask_confirm_password": {
        "uz": "🔁 Yangi parolni <b>qayta kiriting</b> (tasdiqlash):",
        "ru": "🔁 <b>Повторите</b> новый пароль для подтверждения:",
        "en": "🔁 <b>Re-enter</b> the new password to confirm:",
    },
    "pwd_too_short": {
        "uz": "⚠️ Parol kamida 6 belgi bo'lishi kerak. Qayta kiriting:",
        "ru": "⚠️ Пароль должен быть не менее 6 символов. Попробуйте снова:",
        "en": "⚠️ Password must be at least 6 characters. Try again:",
    },
    "pwd_mismatch": {
        "uz": "❌ Parollar mos kelmadi! Yangi parolni kiriting:",
        "ru": "❌ Пароли не совпадают! Введите новый пароль:",
        "en": "❌ Passwords don't match! Enter new password:",
    },
    "pwd_changed": {
        "uz": "✅ Parol muvaffaqiyatli o'zgartirildi!",
        "ru": "✅ Пароль успешно изменён!",
        "en": "✅ Password changed successfully!",
    },

    # ── Statistika ────────────────────────────────────────────────
    "stats": {
        "uz": (
            "📊 <b>Statistika</b>\n\n"
            "👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
            "🆕 Bugun qo'shildi: <b>{new_today}</b>\n"
            "⬇️ Jami yuklamalar: <b>{total_downloads}</b>\n\n"
            "🏆 <b>Top 5 fayl:</b>\n{top_files}"
        ),
        "ru": (
            "📊 <b>Статистика</b>\n\n"
            "👥 Всего пользователей: <b>{total_users}</b>\n"
            "🆕 Новых сегодня: <b>{new_today}</b>\n"
            "⬇️ Всего скачиваний: <b>{total_downloads}</b>\n\n"
            "🏆 <b>Топ 5 файлов:</b>\n{top_files}"
        ),
        "en": (
            "📊 <b>Statistics</b>\n\n"
            "👥 Total users: <b>{total_users}</b>\n"
            "🆕 New today: <b>{new_today}</b>\n"
            "⬇️ Total downloads: <b>{total_downloads}</b>\n\n"
            "🏆 <b>Top 5 files:</b>\n{top_files}"
        ),
    },
}

_LANG_NAMES = {"uz": "O'zbekcha 🇺🇿", "ru": "Русский 🇷🇺", "en": "English 🇬🇧"}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    lang = lang or "uz"
    entry = TEXTS.get(key, {})
    text = entry.get(lang) or entry.get("uz") or key
    if kwargs:
        text = text.format(**kwargs)
    return text


def lang_name(lang: str) -> str:
    return _LANG_NAMES.get(lang or "uz", "O'zbekcha 🇺🇿")
