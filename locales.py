# Faqat O'zbek tili

TEXTS: dict[str, str] = {
    "welcome": (
        "📚 <b>Kutubxona</b>\n\n"
        "Pastdagi menyudan kategoriyani tanlang."
    ),
    "not_subscribed": (
        "⚠️ <b>Botdan foydalanish uchun\n"
        "quyidagi kanallarga obuna bo'ling:</b>"
    ),
    "sub_ok":   "✅ Obuna tasdiqlandi!",
    "sub_fail": "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!",
    "no_files": "😔 Bu kategoriyada hozircha fayllar yo'q.",
    "choose_file": "📄 Faylni tanlang:",
    "downloading": "⬇️ Fayl yuborilmoqda...",
    "file_caption": "📥 <b>{name}</b>\n📂 {category}\n⬇️ Yuklab olindi: <b>{count}</b> marta",

    # Admin — kirish
    "admin_enter_password": (
        "🔐 <b>Admin paneli</b>\n\n"
        "Parolni kiriting:\n"
        "<i>(Bekor qilish: /cancel)</i>"
    ),
    "admin_wrong_password": "❌ Noto'g'ri parol!\n<i>Qolgan urinish: {left}</i>",
    "admin_locked":         "🔒 Juda ko'p noto'g'ri urinish. Keyinroq urinib ko'ring.",
    "admin_logout_done":    "✅ Admin paneldan chiqdingiz.",

    # Admin — panel
    "admin_panel": (
        "⚙️ <b>Admin Panel</b>\n\n"
        "Kategoriyalar, fayllar va kanallarni boshqaring."
    ),

    # Admin — kategoriya
    "ask_cat_name_uz":          "📝 Kategoriya nomini kiriting:\n<i>(/cancel — bekor qilish)</i>",
    "ask_cat_youtube":          "🎬 YouTube havolasini kiriting yoki o'tkazib yuboring:\n<i>Misol: https://youtube.com/playlist?list=...</i>",
    "btn_skip":                 "⏭ O'tkazib yuborish",
    "category_added":           "✅ Kategoriya qo'shildi!",
    "select_category_to_delete":"🗑 <b>O'chiriladigan kategoriyani tanlang:</b>",
    "category_deleted":         "✅ Kategoriya va uning fayllari o'chirildi!",

    # Admin — fayl
    "ask_file_category":    "📂 <b>Qaysi kategoriyaga fayl qo'shilsin?</b>",
    "ask_file_name_uz":     "📝 Fayl nomini kiriting:\n<i>(/cancel — bekor qilish)</i>",
    "ask_upload_file":      "📤 Faylni yuboring:\n<i>Qabul qilinadigan: PDF, RAR, ZIP</i>",
    "wrong_file_type":      "⚠️ Faqat <b>PDF</b>, <b>RAR</b> yoki <b>ZIP</b> fayl yuboring:",
    "file_added":           "✅ Fayl qo'shildi!",
    "select_cat_for_del":   "📂 <b>Qaysi kategoriyadan fayl o'chirilsin?</b>",
    "select_file_to_delete":"🗑 <b>O'chiriladigan faylni tanlang:</b>",
    "file_deleted":         "✅ Fayl o'chirildi!",

    # Admin — kanallar
    "channels_list":            "📢 <b>Majburiy kanallar</b>\n\n{list}\n\nKanal qo'shish yoki o'chirish:",
    "no_channels_yet":          "Hozircha kanallar yo'q.",
    "ask_channel_id": (
        "📢 <b>Kanal ID sini kiriting</b>\n\n"
        "Misol: <code>@kanal_nomi</code> yoki <code>-1001234567890</code>\n\n"
        "<i>⚠️ Bot kanalning admini bo'lishi kerak!</i>"
    ),
    "ask_channel_title":        "✏️ Kanal uchun <b>nom</b> kiriting (tugmada ko'rinadi):",
    "ask_channel_url":          "🔗 Kanal <b>havolasini</b> kiriting:\nMisol: <code>https://t.me/kanal_nomi</code>",
    "channel_added":            "✅ Kanal qo'shildi!",
    "channel_not_accessible": (
        "⚠️ Bot bu kanalga kira olmadi.\n"
        "Bot kanalning admini ekanligini tekshiring va qayta urinib ko'ring:"
    ),
    "select_channel_to_delete": "🗑 <b>O'chiriladigan kanalni tanlang:</b>",
    "channel_deleted":          "✅ Kanal o'chirildi!",

    # Admin — parol
    "ask_new_password":     "🔑 Yangi parolni kiriting <b>(kamida 6 belgi)</b>:\n<i>(/cancel — bekor qilish)</i>",
    "ask_confirm_password": "🔁 Yangi parolni <b>qayta kiriting</b> (tasdiqlash):",
    "pwd_too_short":        "⚠️ Parol kamida 6 belgi bo'lishi kerak. Qayta kiriting:",
    "pwd_mismatch":         "❌ Parollar mos kelmadi! Yangi parolni kiriting:",
    "pwd_changed":          "✅ Parol muvaffaqiyatli o'zgartirildi!",

    # Statistika
    "stats": (
        "📊 <b>Statistika</b>\n\n"
        "👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        "🆕 Bugun qo'shildi: <b>{new_today}</b>\n"
        "⬇️ Jami yuklamalar: <b>{total_downloads}</b>\n\n"
        "🏆 <b>Top 5 fayl:</b>\n{top_files}"
    ),
    "no_categories": "😔 Hozircha kategoriyalar mavjud emas.",
}


def t(key: str, **kwargs) -> str:
    """Matnni kalit bo'yicha qaytaradi (faqat o'zbek tili)."""
    text = TEXTS.get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text