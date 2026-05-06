from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext

import database as db
from locales import t, lang_name
from keyboards import (
    main_reply_keyboard,
    language_inline_keyboard,
    subscribe_inline_keyboard,
    settings_inline_keyboard,
    files_inline_keyboard,
)
from utils import (
    delete_msg, show_panel, clear_panel,
    check_subscription, is_admin,
)

router = Router()

# Barcha tillardagi sozlamalar tugma matnlari (matching uchun)
_SETTINGS_BTNS = {"⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"}
_ADMIN_BTNS    = {"👨‍💼 Admin"}


# ─────────────────────────────────────────────────────────────────
#  Yordamchi: Asosiy menyuni ko'rsatish
# ─────────────────────────────────────────────────────────────────
async def send_main_menu(bot: Bot, chat_id: int, user_id: int, lang: str):
    categories = await db.get_all_categories()
    # Reply keyboard yangilash
    await bot.send_message(
        chat_id,
        t("welcome", lang),
        reply_markup=main_reply_keyboard(categories, lang),
        parse_mode="HTML",
    )


# ─────────────────────────────────────────────────────────────────
#  Obuna tekshiruvi — wrapper
# ─────────────────────────────────────────────────────────────────
async def guard_subscription(bot: Bot, chat_id: int, user_id: int, lang: str) -> bool:
    """
    True — foydalanuvchi barcha kanallarga obuna.
    False — obuna emas, panel xabar ko'rsatildi.
    """
    not_subbed = await check_subscription(bot, user_id)
    if not_subbed:
        await show_panel(
            bot, chat_id, user_id,
            t("not_subscribed", lang),
            subscribe_inline_keyboard(not_subbed, lang),
        )
        return False
    return True


# ═══════════════════════════════════════════════════════
#  /start
# ═══════════════════════════════════════════════════════
@router.message(CommandStart())
async def cmd_start(msg: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await delete_msg(msg)

    user_id = msg.from_user.id
    await db.add_or_update_user(
        user_id,
        msg.from_user.username or "",
        msg.from_user.full_name or "",
    )

    lang = await db.get_user_language(user_id)

    # Birinchi marta: til tanlash
    if lang is None:
        sent = await bot.send_message(
            msg.chat.id,
            "🌐 <b>Tilni tanlang | Выберите язык | Choose language</b>",
            reply_markup=language_inline_keyboard(),
            parse_mode="HTML",
        )
        clear_panel(user_id)
        # Panel sifatida saqla
        from utils import _panel
        _panel[user_id] = sent.message_id
        return

    await send_main_menu(bot, msg.chat.id, user_id, lang)


# ═══════════════════════════════════════════════════════
#  TIL TANLASH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data.startswith("lang:"))
async def set_language(call: CallbackQuery, bot: Bot):
    lang = call.data.split(":")[1]
    user_id = call.from_user.id
    await db.set_user_language(user_id, lang)
    await call.answer(t("language_set", lang))

    # Panel xabarini o'chirib, asosiy menyuni yuboramiz
    await delete_msg(call.message)
    clear_panel(user_id)
    await send_main_menu(bot, call.message.chat.id, user_id, lang)


@router.callback_query(F.data == "change_language")
async def change_language(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await db.get_user_language(user_id) or "uz"
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("choose_language", lang),
        language_inline_keyboard(),
    )
    await call.answer()


# ═══════════════════════════════════════════════════════
#  OBUNA TEKSHIRUVI (callback)
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "check_subscription")
async def check_sub_callback(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await db.get_user_language(user_id) or "uz"

    not_subbed = await check_subscription(bot, user_id)
    if not_subbed:
        await call.answer(t("sub_fail", lang), show_alert=True)
        await show_panel(
            bot, call.message.chat.id, user_id,
            t("not_subscribed", lang),
            subscribe_inline_keyboard(not_subbed, lang),
        )
    else:
        await call.answer(t("sub_ok", lang), show_alert=True)
        await delete_msg(call.message)
        clear_panel(user_id)
        await send_main_menu(bot, call.message.chat.id, user_id, lang)


# ═══════════════════════════════════════════════════════
#  PANEL YOPISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "close_panel")
async def close_panel(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    await delete_msg(call.message)
    clear_panel(user_id)
    await call.answer()


# ═══════════════════════════════════════════════════════
#  FAYL YUKLASH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data.startswith("file:"))
async def send_file(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await db.get_user_language(user_id) or "uz"

    # Obuna tekshiruvi
    if not await guard_subscription(bot, call.message.chat.id, user_id, lang):
        await call.answer()
        return

    file_id = int(call.data.split(":")[1])
    file    = await db.get_file_by_id(file_id)
    if not file:
        await call.answer("❌ Fayl topilmadi!", show_alert=True)
        return

    await call.answer(t("downloading", lang))

    cat      = await db.get_category_by_id(file["category_id"])
    name     = file.get(f"name_{lang}") or file["name_uz"]
    cat_name = (cat.get(f"name_{lang}") or cat["name_uz"]) if cat else "—"

    caption = t("file_caption", lang,
                name=name,
                category=cat_name,
                count=file["download_count"] + 1)

    await bot.send_document(
        call.message.chat.id,
        document=file["file_id"],
        caption=caption,
        parse_mode="HTML",
    )
    await db.increment_download(file_id, user_id)


# ═══════════════════════════════════════════════════════
#  REPLY KEYBOARD — MATN XABARLARI (FSM holati yo'q)
# ═══════════════════════════════════════════════════════
@router.message(F.text, StateFilter(None))
async def handle_reply_buttons(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    text    = msg.text.strip()
    await delete_msg(msg)

    lang = await db.get_user_language(user_id) or "uz"

    # ── Obuna tekshiruvi ──
    if not await guard_subscription(bot, msg.chat.id, user_id, lang):
        return

    # ── Sozlamalar ──
    if text in _SETTINGS_BTNS:
        await show_panel(
            bot, msg.chat.id, user_id,
            t("settings_title", lang, lang_name=lang_name(lang)),
            settings_inline_keyboard(lang),
        )
        return

    # ── Admin tugmasi ──
    if text in _ADMIN_BTNS:
        if is_admin(user_id):
            from keyboards import admin_panel_inline_keyboard
            await show_panel(
                bot, msg.chat.id, user_id,
                t("admin_panel", lang),
                admin_panel_inline_keyboard(lang),
            )
        else:
            # Parol so'raymiz — AdminLogin FSM boshlaymiz
            from admin import AdminLogin
            from utils import is_locked
            if is_locked(user_id):
                await show_panel(bot, msg.chat.id, user_id, t("admin_locked", lang))
                return
            await state.set_state(AdminLogin.password)
            await show_panel(
                bot, msg.chat.id, user_id,
                t("admin_enter_password", lang),
                None,
            )
        return

    # ── Kategoriya ──
    categories = await db.get_all_categories()
    matched = None
    for cat in categories:
        for l in ("uz", "ru", "en"):
            cat_name = cat.get(f"name_{l}") or cat["name_uz"]
            if text == f"📂 {cat_name}":
                matched = cat
                break
        if matched:
            break

    if matched:
        files    = await db.get_files_by_category(matched["id"])
        cat_name = matched.get(f"name_{lang}") or matched["name_uz"]
        if not files:
            await show_panel(
                bot, msg.chat.id, user_id,
                f"📂 <b>{cat_name}</b>\n\n{t('no_files', lang)}",
                None,
            )
        else:
            await show_panel(
                bot, msg.chat.id, user_id,
                f"📂 <b>{cat_name}</b>\n\n{t('choose_file', lang)}",
                files_inline_keyboard(files, lang),
            )
