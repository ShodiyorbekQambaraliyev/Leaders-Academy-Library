from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext

import database as db
from locales import t
from keyboards import (
    main_reply_keyboard,
    subscribe_inline_keyboard,
    files_inline_keyboard,
    admin_panel_inline_keyboard,
    cat_btn_text,
)
from utils import (
    delete_msg, show_panel, clear_panel,
    check_subscription, is_admin, is_locked,
)

router = Router()

_ADMIN_BTN = "👨‍💼 Admin"


# ─── Yordamchi ────────────────────────────────────────────────────────────────

async def send_main_menu(bot: Bot, chat_id: int, user_id: int):
    """Reply keyboardli asosiy menyuni yuboradi."""
    categories = await db.get_all_categories()
    await bot.send_message(
        chat_id,
        t("welcome"),
        reply_markup=main_reply_keyboard(categories),
        parse_mode="HTML",
    )


async def guard_subscription(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    True  → foydalanuvchi barcha kanallarga obuna.
    False → obuna emas, panel ko'rsatildi.
    """
    not_subbed = await check_subscription(bot, user_id)
    if not_subbed:
        await show_panel(
            bot, chat_id, user_id,
            t("not_subscribed"),
            subscribe_inline_keyboard(not_subbed),
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
    # Til faqat UZ bo'ladi (agar DB da yo'q bo'lsa o'rnatamiz)
    lang = await db.get_user_language(user_id)
    if lang is None:
        await db.set_user_language(user_id, "uz")

    await send_main_menu(bot, msg.chat.id, user_id)


# ═══════════════════════════════════════════════════════
#  OBUNA TEKSHIRUVI (callback)
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "check_subscription")
async def check_sub_callback(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id

    not_subbed = await check_subscription(bot, user_id)
    if not_subbed:
        await call.answer(t("sub_fail"), show_alert=True)
        await show_panel(
            bot, call.message.chat.id, user_id,
            t("not_subscribed"),
            subscribe_inline_keyboard(not_subbed),
        )
    else:
        await call.answer(t("sub_ok"), show_alert=True)
        await delete_msg(call.message)
        clear_panel(user_id)
        await send_main_menu(bot, call.message.chat.id, user_id)


# ═══════════════════════════════════════════════════════
#  PANEL YOPISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "close_panel")
async def close_panel_cb(call: CallbackQuery, bot: Bot):
    await delete_msg(call.message)
    clear_panel(call.from_user.id)
    await call.answer()


# ═══════════════════════════════════════════════════════
#  FAYL YUKLASH
#  → Fayl yuborilgandan so'ng panel o'chiriladi.
#    Keyingi fayl olish uchun kategoriyani qayta tanlash kerak.
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data.startswith("file:"))
async def send_file(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id

    if not await guard_subscription(bot, call.message.chat.id, user_id):
        await call.answer()
        return

    file_id = int(call.data.split(":")[1])
    file    = await db.get_file_by_id(file_id)
    if not file:
        await call.answer("❌ Fayl topilmadi!", show_alert=True)
        return

    await call.answer(t("downloading"))

    cat      = await db.get_category_by_id(file["category_id"])
    name     = file["name_uz"]
    cat_name = cat["name_uz"] if cat else "—"
    caption  = t("file_caption", name=name, category=cat_name)

    # 1. Faylni yuboramiz
    await bot.send_document(
        call.message.chat.id,
        document=file["file_id"],
        caption=caption,
        parse_mode="HTML",
    )
    await db.increment_download(file_id, user_id)

    # 2. Yuqoridagi panel xabarini (fayllar ro'yxati) o'chiramiz
    await delete_msg(call.message)
    clear_panel(user_id)


# ═══════════════════════════════════════════════════════
#  REPLY KEYBOARD — matn xabarlari (FSM holati yo'q)
# ═══════════════════════════════════════════════════════
@router.message(F.text, StateFilter(None))
async def handle_reply_buttons(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    text    = msg.text.strip()
    await delete_msg(msg)

    if not await guard_subscription(bot, msg.chat.id, user_id):
        return

    # ── Admin tugmasi ──────────────────────────────────────────────
    if text == _ADMIN_BTN:
        if is_admin(user_id):
            await show_panel(
                bot, msg.chat.id, user_id,
                t("admin_panel"),
                admin_panel_inline_keyboard(),
            )
        else:
            if is_locked(user_id):
                await show_panel(bot, msg.chat.id, user_id, t("admin_locked"))
                return
            from admin import AdminLogin
            await state.set_state(AdminLogin.password)
            await show_panel(
                bot, msg.chat.id, user_id,
                t("admin_enter_password"),
            )
        return

    # ── Kategoriya tugmasi ─────────────────────────────────────────
    categories = await db.get_all_categories()
    matched = None
    for i, cat in enumerate(categories):
        if text == cat_btn_text(cat, i):
            matched = cat
            break

    if matched:
        files = await db.get_files_by_category(matched["id"])
        youtube_url = matched.get("youtube_url")
        if not files:
            await show_panel(
                bot, msg.chat.id, user_id,
                f"📗 <b>{matched['name_uz']}</b>\n\n{t('no_files')}",
            )
        else:
            await show_panel(
                bot, msg.chat.id, user_id,
                f"📗 <b>{matched['name_uz']}</b>\n\n{t('choose_file')}",
                files_inline_keyboard(files, youtube_url),
            )