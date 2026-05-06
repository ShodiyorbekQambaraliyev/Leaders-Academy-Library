from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, Document
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import database as db
from locales import t
from keyboards import (
    admin_panel_inline_keyboard,
    admin_cancel_inline_keyboard,
    admin_back_inline_keyboard,
    admin_categories_inline_keyboard,
    admin_files_inline_keyboard,
    admin_channels_inline_keyboard,
    admin_del_channels_inline_keyboard,
    main_reply_keyboard,
)
from utils import (
    delete_msg, show_panel, clear_panel,
    is_admin, auth_admin, deauth_admin,
    get_attempts, inc_attempts, reset_attempts, is_locked,
    MAX_ATTEMPTS,
)

router = Router()

ALLOWED_MIME: dict[str, str] = {
    "application/pdf":              "pdf",
    "application/x-rar-compressed": "rar",
    "application/vnd.rar":          "rar",
    "application/zip":              "zip",
    "application/x-zip-compressed": "zip",
    "application/octet-stream":     "rar",
}


# ═══════════════════════════════════════════════════════
#  FSM HOLATLARI
# ═══════════════════════════════════════════════════════
class AdminLogin(StatesGroup):
    password = State()


class AdminChangePwd(StatesGroup):
    new_pwd     = State()
    confirm_pwd = State()


class AddCategory(StatesGroup):
    name_uz = State()
    name_ru = State()
    name_en = State()


class AddFile(StatesGroup):
    category = State()
    name_uz  = State()
    name_ru  = State()
    name_en  = State()
    upload   = State()


class AddChannel(StatesGroup):
    channel_id = State()
    title      = State()
    url        = State()


# ─────────────────────────────────────────────────────────────────
#  Yordamchi
# ─────────────────────────────────────────────────────────────────
async def get_lang(user_id: int) -> str:
    return await db.get_user_language(user_id) or "uz"


async def back_to_admin(bot: Bot, chat_id: int, user_id: int, lang: str):
    """Admin panelini qaytadan ko'rsatadi."""
    await show_panel(
        bot, chat_id, user_id,
        t("admin_panel", lang),
        admin_panel_inline_keyboard(lang),
    )


# ═══════════════════════════════════════════════════════
#  /cancel — FSM ni to'xtatish
# ═══════════════════════════════════════════════════════
@router.message(Command("cancel"))
async def cmd_cancel(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    await state.clear()
    await delete_msg(msg)
    if is_admin(user_id):
        await back_to_admin(bot, msg.chat.id, user_id, lang)


# ═══════════════════════════════════════════════════════
#  ADMIN LOGIN — Parol tekshiruvi
# ═══════════════════════════════════════════════════════
@router.message(AdminLogin.password)
async def check_password(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    entered = msg.text.strip() if msg.text else ""
    await delete_msg(msg)   # Parolni darhol o'chiramiz!

    if is_locked(user_id):
        await state.clear()
        await show_panel(bot, msg.chat.id, user_id, t("admin_locked", lang))
        return

    correct = await db.get_admin_password()
    if entered == correct:
        auth_admin(user_id)
        await state.clear()
        await show_panel(
            bot, msg.chat.id, user_id,
            t("admin_panel", lang),
            admin_panel_inline_keyboard(lang),
        )
    else:
        attempts = inc_attempts(user_id)
        left     = MAX_ATTEMPTS - attempts
        if left <= 0:
            await state.clear()
            await show_panel(bot, msg.chat.id, user_id, t("admin_locked", lang))
        else:
            await show_panel(
                bot, msg.chat.id, user_id,
                t("admin_wrong_password", lang, left=left),
            )


# ═══════════════════════════════════════════════════════
#  ADMIN CALLBACK — umumiy
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:back")
async def adm_back(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return
    await back_to_admin(bot, call.message.chat.id, user_id, lang)
    await call.answer()


@router.callback_query(F.data == "adm:cancel")
async def adm_cancel(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    await state.clear()
    if not is_admin(user_id):
        await call.answer()
        return
    await back_to_admin(bot, call.message.chat.id, user_id, lang)
    await call.answer()


@router.callback_query(F.data == "adm:logout")
async def adm_logout(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    await state.clear()
    deauth_admin(user_id)
    await show_panel(bot, call.message.chat.id, user_id, t("admin_logout_done", lang))
    await call.answer()


# ═══════════════════════════════════════════════════════
#  STATISTIKA
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:stats")
async def adm_stats(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    total_users  = await db.get_total_users()
    new_today    = await db.get_new_users_today()
    total_dl     = await db.get_total_downloads()
    top_files    = await db.get_top_files(5)

    top_str = ""
    for i, f in enumerate(top_files, 1):
        name = f.get(f"name_{lang}") or f["name_uz"]
        top_str += f"{i}. {name} — {f['download_count']}⬇️\n"
    if not top_str:
        top_str = "—"

    await show_panel(
        bot, call.message.chat.id, user_id,
        t("stats", lang,
          total_users=total_users,
          new_today=new_today,
          total_downloads=total_dl,
          top_files=top_str),
        admin_back_inline_keyboard(lang),
    )
    await call.answer()


# ═══════════════════════════════════════════════════════
#  PAROL O'ZGARTIRISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:change_pwd")
async def adm_change_pwd_start(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return
    await state.set_state(AdminChangePwd.new_pwd)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("ask_new_password", lang),
        admin_cancel_inline_keyboard(lang),
    )
    await call.answer()


@router.message(AdminChangePwd.new_pwd)
async def adm_change_pwd_new(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    new_pwd = msg.text.strip() if msg.text else ""
    await delete_msg(msg)

    if len(new_pwd) < 6:
        await show_panel(
            bot, msg.chat.id, user_id,
            t("pwd_too_short", lang),
            admin_cancel_inline_keyboard(lang),
        )
        return

    await state.update_data(new_pwd=new_pwd)
    await state.set_state(AdminChangePwd.confirm_pwd)
    await show_panel(
        bot, msg.chat.id, user_id,
        t("ask_confirm_password", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AdminChangePwd.confirm_pwd)
async def adm_change_pwd_confirm(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    confirm = msg.text.strip() if msg.text else ""
    await delete_msg(msg)

    data    = await state.get_data()
    new_pwd = data.get("new_pwd", "")

    if confirm != new_pwd:
        await state.set_state(AdminChangePwd.new_pwd)
        await show_panel(
            bot, msg.chat.id, user_id,
            t("pwd_mismatch", lang),
            admin_cancel_inline_keyboard(lang),
        )
        return

    await db.set_admin_password(new_pwd)
    await state.clear()
    await show_panel(
        bot, msg.chat.id, user_id,
        t("pwd_changed", lang) + "\n\n" + t("admin_panel", lang),
        admin_panel_inline_keyboard(lang),
    )


# ═══════════════════════════════════════════════════════
#  KATEGORIYA QO'SHISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:add_cat")
async def adm_add_cat_start(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return
    await state.set_state(AddCategory.name_uz)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("ask_cat_name_uz", lang),
        admin_cancel_inline_keyboard(lang),
    )
    await call.answer()


@router.message(AddCategory.name_uz)
async def adm_cat_name_uz(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await state.update_data(name_uz=msg.text.strip())
    await delete_msg(msg)
    await state.set_state(AddCategory.name_ru)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("ask_cat_name_ru", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddCategory.name_ru)
async def adm_cat_name_ru(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await state.update_data(name_ru=msg.text.strip())
    await delete_msg(msg)
    await state.set_state(AddCategory.name_en)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("ask_cat_name_en", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddCategory.name_en)
async def adm_cat_name_en(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    data    = await state.get_data()
    await db.add_category(data["name_uz"], data["name_ru"], msg.text.strip())
    await delete_msg(msg)
    await state.clear()

    # Reply keyboard yangilash
    categories = await db.get_all_categories()
    await bot.send_message(
        msg.chat.id,
        t("category_added", lang),
        reply_markup=main_reply_keyboard(categories, lang),
        parse_mode="HTML",
    )
    clear_panel(user_id)
    await back_to_admin(bot, msg.chat.id, user_id, lang)


# ═══════════════════════════════════════════════════════
#  KATEGORIYA O'CHIRISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:del_cat")
async def adm_del_cat_start(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    categories = await db.get_all_categories()
    if not categories:
        await call.answer(t("no_categories", lang), show_alert=True)
        return

    await show_panel(
        bot, call.message.chat.id, user_id,
        t("select_category_to_delete", lang),
        admin_categories_inline_keyboard(categories, lang, "delcat"),
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_delcat:"))
async def adm_del_cat_confirm(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    cat_id = int(call.data.split(":")[1])
    await db.delete_category(cat_id)

    # Reply keyboard yangilash
    categories = await db.get_all_categories()
    await bot.send_message(
        call.message.chat.id,
        t("category_deleted", lang),
        reply_markup=main_reply_keyboard(categories, lang),
        parse_mode="HTML",
    )
    clear_panel(user_id)
    await back_to_admin(bot, call.message.chat.id, user_id, lang)
    await call.answer()


# ═══════════════════════════════════════════════════════
#  FAYL QO'SHISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:add_file")
async def adm_add_file_start(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    categories = await db.get_all_categories()
    if not categories:
        await call.answer(t("no_categories", lang), show_alert=True)
        return

    await state.set_state(AddFile.category)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("ask_file_category", lang),
        admin_categories_inline_keyboard(categories, lang, "selcat"),
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_selcat:"))
async def adm_file_cat_selected(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    cat_id  = int(call.data.split(":")[1])
    await state.update_data(category_id=cat_id)
    await state.set_state(AddFile.name_uz)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("ask_file_name_uz", lang),
        admin_cancel_inline_keyboard(lang),
    )
    await call.answer()


@router.message(AddFile.name_uz)
async def adm_file_name_uz(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await state.update_data(name_uz=msg.text.strip())
    await delete_msg(msg)
    await state.set_state(AddFile.name_ru)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("ask_file_name_ru", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddFile.name_ru)
async def adm_file_name_ru(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await state.update_data(name_ru=msg.text.strip())
    await delete_msg(msg)
    await state.set_state(AddFile.name_en)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("ask_file_name_en", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddFile.name_en)
async def adm_file_name_en(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await state.update_data(name_en=msg.text.strip())
    await delete_msg(msg)
    await state.set_state(AddFile.upload)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("ask_upload_file", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddFile.upload, F.document)
async def adm_file_uploaded(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    doc: Document = msg.document

    mime      = doc.mime_type or ""
    file_type = ALLOWED_MIME.get(mime)

    if not file_type and doc.file_name:
        fn = doc.file_name.lower()
        if fn.endswith(".pdf"):
            file_type = "pdf"
        elif fn.endswith(".zip"):
            file_type = "zip"
        elif fn.endswith(".rar"):
            file_type = "rar"

    if not file_type:
        await delete_msg(msg)
        await show_panel(
            bot, msg.chat.id, user_id,
            t("wrong_file_type", lang),
            admin_cancel_inline_keyboard(lang),
        )
        return

    data = await state.get_data()
    await db.add_file(
        category_id=data["category_id"],
        name_uz=data["name_uz"],
        name_ru=data["name_ru"],
        name_en=data["name_en"],
        file_id=doc.file_id,
        file_type=file_type,
    )
    await delete_msg(msg)
    await state.clear()
    await show_panel(
        bot, msg.chat.id, user_id,
        t("file_added", lang) + "\n\n" + t("admin_panel", lang),
        admin_panel_inline_keyboard(lang),
    )


@router.message(AddFile.upload)
async def adm_wrong_upload(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await delete_msg(msg)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("wrong_file_type", lang),
        admin_cancel_inline_keyboard(lang),
    )


# ═══════════════════════════════════════════════════════
#  FAYL O'CHIRISH
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:del_file")
async def adm_del_file_start(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    categories = await db.get_all_categories()
    if not categories:
        await call.answer(t("no_categories", lang), show_alert=True)
        return

    await show_panel(
        bot, call.message.chat.id, user_id,
        t("select_cat_for_del_file", lang),
        admin_categories_inline_keyboard(categories, lang, "delfilecat"),
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_delfilecat:"))
async def adm_del_file_cat_selected(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    cat_id = int(call.data.split(":")[1])
    files  = await db.get_files_by_category(cat_id)
    if not files:
        await call.answer(t("no_files", lang), show_alert=True)
        return

    await show_panel(
        bot, call.message.chat.id, user_id,
        t("select_file_to_delete", lang),
        admin_files_inline_keyboard(files, lang),
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_delfile:"))
async def adm_del_file_confirm(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    file_id = int(call.data.split(":")[1])
    await db.delete_file(file_id)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("file_deleted", lang) + "\n\n" + t("admin_panel", lang),
        admin_panel_inline_keyboard(lang),
    )
    await call.answer()


# ═══════════════════════════════════════════════════════
#  KANALLAR
# ═══════════════════════════════════════════════════════
@router.callback_query(F.data == "adm:channels")
async def adm_channels(call: CallbackQuery, bot: Bot):
    user_id  = call.from_user.id
    lang     = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    channels = await db.get_required_channels()
    ch_list  = ""
    for i, ch in enumerate(channels, 1):
        ch_list += f"{i}. <b>{ch['title']}</b> — <code>{ch['channel_id']}</code>\n"
    if not ch_list:
        ch_list = t("no_channels_yet", lang)

    await show_panel(
        bot, call.message.chat.id, user_id,
        t("channels_list", lang, list=ch_list),
        admin_channels_inline_keyboard(channels, lang),
    )
    await call.answer()


# ── Kanal qo'shish ──
@router.callback_query(F.data == "adm:add_channel")
async def adm_add_channel_start(call: CallbackQuery, bot: Bot, state: FSMContext):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return
    await state.set_state(AddChannel.channel_id)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("ask_channel_id", lang),
        admin_cancel_inline_keyboard(lang),
    )
    await call.answer()


@router.message(AddChannel.channel_id)
async def adm_add_channel_id(msg: Message, bot: Bot, state: FSMContext):
    user_id    = msg.from_user.id
    lang       = await get_lang(user_id)
    channel_id = msg.text.strip()
    await delete_msg(msg)

    # Botning kanalga kirishini tekshir
    try:
        chat = await bot.get_chat(channel_id)
        real_id = str(chat.id)
    except Exception:
        await show_panel(
            bot, msg.chat.id, user_id,
            t("channel_not_accessible", lang),
            admin_cancel_inline_keyboard(lang),
        )
        return

    await state.update_data(channel_id=real_id)
    await state.set_state(AddChannel.title)
    await show_panel(
        bot, msg.chat.id, user_id,
        t("ask_channel_title", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddChannel.title)
async def adm_add_channel_title(msg: Message, bot: Bot, state: FSMContext):
    lang = await get_lang(msg.from_user.id)
    await state.update_data(title=msg.text.strip())
    await delete_msg(msg)
    await state.set_state(AddChannel.url)
    await show_panel(
        bot, msg.chat.id, msg.from_user.id,
        t("ask_channel_url", lang),
        admin_cancel_inline_keyboard(lang),
    )


@router.message(AddChannel.url)
async def adm_add_channel_url(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    lang    = await get_lang(user_id)
    url     = msg.text.strip()
    await delete_msg(msg)

    data = await state.get_data()
    await db.add_required_channel(data["channel_id"], data["title"], url)
    await state.clear()
    await show_panel(
        bot, msg.chat.id, user_id,
        t("channel_added", lang) + "\n\n" + t("admin_panel", lang),
        admin_panel_inline_keyboard(lang),
    )


# ── Kanal o'chirish ──
@router.callback_query(F.data == "adm:del_channel")
async def adm_del_channel_start(call: CallbackQuery, bot: Bot):
    user_id  = call.from_user.id
    lang     = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    channels = await db.get_required_channels()
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("select_channel_to_delete", lang),
        admin_del_channels_inline_keyboard(channels, lang),
    )
    await call.answer()


@router.callback_query(F.data.startswith("adm_delch:"))
async def adm_del_channel_confirm(call: CallbackQuery, bot: Bot):
    user_id = call.from_user.id
    lang    = await get_lang(user_id)
    if not is_admin(user_id):
        await call.answer()
        return

    ch_row_id = int(call.data.split(":")[1])
    await db.delete_required_channel(ch_row_id)
    await show_panel(
        bot, call.message.chat.id, user_id,
        t("channel_deleted", lang) + "\n\n" + t("admin_panel", lang),
        admin_panel_inline_keyboard(lang),
    )
    await call.answer()
