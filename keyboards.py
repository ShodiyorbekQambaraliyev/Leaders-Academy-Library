from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
)

# ─── Kitob ranglari (kategoriya tartibiga qarab sikl qiladi) ────────────────
BOOK_COLORS = ["📗", "📘", "📙", "📕"]

# ─── Raqamli emojilar 1️⃣ … 🔟, undan keyin oddiy raqam ───────────────────
NUM_EMOJIS = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

def _book(index: int) -> str:
    return BOOK_COLORS[index % len(BOOK_COLORS)]

def _num(index: int) -> str:
    return NUM_EMOJIS[index] if index < len(NUM_EMOJIS) else str(index + 1)

def cat_btn_text(cat: dict, index: int) -> str:
    """Kategoriya tugmasi matni: 📗 Nom 1️⃣"""
    return f"{_book(index)} {cat['name_uz']} {_num(index)}"


# ═══════════════════════════════════════════════
#  REPLY KEYBOARD (pastki doimiy menyu)
#  — Har kategoriya ALOHIDA qatorda
#  — Oxirida Admin tugmasi
# ═══════════════════════════════════════════════

def main_reply_keyboard(categories: list[dict]) -> ReplyKeyboardMarkup:
    rows: list[list[KeyboardButton]] = []
    for i, cat in enumerate(categories):
        rows.append([KeyboardButton(text=cat_btn_text(cat, i))])
    rows.append([KeyboardButton(text="👨‍💼 Admin")])
    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        is_persistent=True,
    )


# ═══════════════════════════════════════════════
#  INLINE — OBUNA
# ═══════════════════════════════════════════════

def subscribe_inline_keyboard(channels: list[dict]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"📢 {ch['title']}", url=ch["url"])]
        for ch in channels
    ]
    rows.append([InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def skip_inline_keyboard() -> InlineKeyboardMarkup:
    """YouTube URLni o'tkazib yuborish tugmasi."""
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭ O'tkazib yuborish", callback_data="adm:skip_youtube")],
        [InlineKeyboardButton(text="❌ Bekor qilish",      callback_data="adm:cancel")],
    ])


# ═══════════════════════════════════════════════
#  INLINE — FAYLLAR RO'YXATI
#  — Har fayl ALOHIDA qatorda
#  — Fayllar uchun keyingi daraja kitob rangi (📘 PDF, 📙 RAR/ZIP)
#  — Agar kategoriyada youtube_url bo'lsa — YouTube tugmasi
# ═══════════════════════════════════════════════

def files_inline_keyboard(files: list[dict], youtube_url: str | None = None) -> InlineKeyboardMarkup:
    rows = []
    # YouTube havolasi bo'lsa — birinchi tugma sifatida qo'shamiz
    if youtube_url:
        rows.append([InlineKeyboardButton(
            text="▶️ YouTube da ko'rish",
            url=youtube_url,
        )])
    for f in files:
        # Fayl turi bo'yicha rang: PDF → 📘, arxiv → 📙
        icon = "📘" if f["file_type"] == "pdf" else "📙"
        name = f["name_uz"]
        rows.append([InlineKeyboardButton(
            text=f"{icon} {name}  ({f['download_count']}⬇️)",
            callback_data=f"file:{f['id']}",
        )])
    rows.append([InlineKeyboardButton(text="❌ Yopish", callback_data="close_panel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ═══════════════════════════════════════════════
#  INLINE — ADMIN PANEL
#  — Har tugma ALOHIDA qatorda
# ═══════════════════════════════════════════════

def admin_panel_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Kategoriya qo'shish", callback_data="adm:add_cat")],
        [InlineKeyboardButton(text="🗑 Kategoriya o'chirish",  callback_data="adm:del_cat")],
        [InlineKeyboardButton(text="📤 Fayl qo'shish",        callback_data="adm:add_file")],
        [InlineKeyboardButton(text="🗑 Fayl o'chirish",        callback_data="adm:del_file")],
        [InlineKeyboardButton(text="📢 Kanallar",              callback_data="adm:channels")],
        [InlineKeyboardButton(text="📊 Statistika",            callback_data="adm:stats")],
        [InlineKeyboardButton(text="🔑 Parol o'zgartirish",   callback_data="adm:change_pwd")],
        [InlineKeyboardButton(text="🚪 Chiqish",               callback_data="adm:logout")],
    ])


def admin_cancel_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm:cancel"),
    ]])


def admin_back_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="⬅️ Admin panel", callback_data="adm:back"),
    ]])


def admin_categories_inline_keyboard(categories: list[dict], action: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=cat_btn_text(cat, i),
            callback_data=f"adm_{action}:{cat['id']}",
        )]
        for i, cat in enumerate(categories)
    ]
    rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_files_inline_keyboard(files: list[dict]) -> InlineKeyboardMarkup:
    rows = []
    for f in files:
        icon = "📘" if f["file_type"] == "pdf" else "📙"
        rows.append([InlineKeyboardButton(
            text=f"{icon} {f['name_uz']}",
            callback_data=f"adm_delfile:{f['id']}",
        )])
    rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_channels_inline_keyboard(channels: list[dict]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text="➕ Kanal qo'shish", callback_data="adm:add_channel")],
    ]
    if channels:
        rows.append([InlineKeyboardButton(text="🗑 Kanal o'chirish", callback_data="adm:del_channel")])
    rows.append([InlineKeyboardButton(text="⬅️ Admin panel", callback_data="adm:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_del_channels_inline_keyboard(channels: list[dict]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"📢 {ch['title']}",
            callback_data=f"adm_delch:{ch['id']}",
        )]
        for ch in channels
    ]
    rows.append([InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm:channels")])
    return InlineKeyboardMarkup(inline_keyboard=rows)