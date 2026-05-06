from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
)
from locales import t


# ═══════════════════════════════════════════════
#  REPLY KEYBOARD (pastki menyu)
# ═══════════════════════════════════════════════

def main_reply_keyboard(categories: list[dict], lang: str) -> ReplyKeyboardMarkup:
    """
    Pastki doimiy menyu:
      - Har qatorda 2 ta kategoriya
      - Oxirgi qatorda: Sozlamalar | Admin
    """
    rows: list[list[KeyboardButton]] = []

    # Kategoriyalar — 2 tadan qatorda
    pair: list[KeyboardButton] = []
    for cat in categories:
        name = cat.get(f"name_{lang}") or cat["name_uz"]
        pair.append(KeyboardButton(text=f"📂 {name}"))
        if len(pair) == 2:
            rows.append(pair)
            pair = []
    if pair:
        rows.append(pair)

    # Sozlamalar + Admin qatori
    rows.append([
        KeyboardButton(text=t("btn_settings_reply", lang)),
        KeyboardButton(text=t("btn_admin_reply", lang)),
    ])

    return ReplyKeyboardMarkup(
        keyboard=rows,
        resize_keyboard=True,
        is_persistent=True,
    )


# ═══════════════════════════════════════════════
#  INLINE — TIL TANLASH
# ═══════════════════════════════════════════════

def language_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="lang:uz"),
        InlineKeyboardButton(text="🇷🇺 Русский",   callback_data="lang:ru"),
        InlineKeyboardButton(text="🇬🇧 English",   callback_data="lang:en"),
    ]])


# ═══════════════════════════════════════════════
#  INLINE — OBUNA
# ═══════════════════════════════════════════════

def subscribe_inline_keyboard(channels: list[dict], lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"📢 {ch['title']}", url=ch["url"])]
        for ch in channels
    ]
    rows.append([InlineKeyboardButton(
        text=t("btn_check_sub", lang),
        callback_data="check_subscription",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ═══════════════════════════════════════════════
#  INLINE — SOZLAMALAR
# ═══════════════════════════════════════════════

def settings_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t("btn_change_lang", lang), callback_data="change_language")],
        [InlineKeyboardButton(text=t("btn_close",       lang), callback_data="close_panel")],
    ])


# ═══════════════════════════════════════════════
#  INLINE — FAYLLAR RO'YXATI
# ═══════════════════════════════════════════════

def files_inline_keyboard(files: list[dict], lang: str) -> InlineKeyboardMarkup:
    rows = []
    for f in files:
        name = f.get(f"name_{lang}") or f["name_uz"]
        icon = "📄" if f["file_type"] == "pdf" else "📦"
        rows.append([InlineKeyboardButton(
            text=f"{icon} {name}  ({f['download_count']}⬇️)",
            callback_data=f"file:{f['id']}",
        )])
    rows.append([InlineKeyboardButton(
        text=t("btn_back_cats", lang),
        callback_data="close_panel",
    )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


# ═══════════════════════════════════════════════
#  INLINE — ADMIN PANEL
# ═══════════════════════════════════════════════

def admin_panel_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=t("btn_add_category", lang), callback_data="adm:add_cat"),
            InlineKeyboardButton(text=t("btn_del_category", lang), callback_data="adm:del_cat"),
        ],
        [
            InlineKeyboardButton(text=t("btn_add_file",     lang), callback_data="adm:add_file"),
            InlineKeyboardButton(text=t("btn_del_file",     lang), callback_data="adm:del_file"),
        ],
        [
            InlineKeyboardButton(text=t("btn_channels",     lang), callback_data="adm:channels"),
            InlineKeyboardButton(text=t("btn_stats",        lang), callback_data="adm:stats"),
        ],
        [
            InlineKeyboardButton(text=t("btn_change_pwd",   lang), callback_data="adm:change_pwd"),
            InlineKeyboardButton(text=t("btn_logout",       lang), callback_data="adm:logout"),
        ],
    ])


def admin_cancel_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="adm:cancel"),
    ]])


def admin_back_inline_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t("btn_back_admin", lang), callback_data="adm:back"),
    ]])


def admin_categories_inline_keyboard(
    categories: list[dict], lang: str, action: str
) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"📂 {cat.get(f'name_{lang}') or cat['name_uz']}",
            callback_data=f"adm_{action}:{cat['id']}",
        )]
        for cat in categories
    ]
    rows.append([InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="adm:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_files_inline_keyboard(files: list[dict], lang: str) -> InlineKeyboardMarkup:
    rows = []
    for f in files:
        name = f.get(f"name_{lang}") or f["name_uz"]
        icon = "📄" if f["file_type"] == "pdf" else "📦"
        rows.append([InlineKeyboardButton(
            text=f"{icon} {name}",
            callback_data=f"adm_delfile:{f['id']}",
        )])
    rows.append([InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="adm:cancel")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_channels_inline_keyboard(channels: list[dict], lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=t("btn_add_channel", lang), callback_data="adm:add_channel")],
    ]
    if channels:
        rows.append([InlineKeyboardButton(text=t("btn_del_channel", lang), callback_data="adm:del_channel")])
    rows.append([InlineKeyboardButton(text=t("btn_back_admin", lang), callback_data="adm:back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_del_channels_inline_keyboard(channels: list[dict], lang: str) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(
            text=f"📢 {ch['title']}",
            callback_data=f"adm_delch:{ch['id']}",
        )]
        for ch in channels
    ]
    rows.append([InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="adm:channels")])
    return InlineKeyboardMarkup(inline_keyboard=rows)
