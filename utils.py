from __future__ import annotations
from aiogram import Bot
import database as db
from config import ADMIN_IDS

# ─── Panel xabar kuzatuvi (user_id → message_id) ─────────────────────────────
# Bot har bir foydalanuvchi uchun bitta "panel" xabarini saqlaydi va uni tahrirlaydi.
_panel: dict[int, int] = {}

# ─── Admin sessiyalari ────────────────────────────────────────────────────────
_authed_admins: set[int] = set()
_failed_attempts: dict[int, int] = {}
MAX_ATTEMPTS = 5


# ─── Admin autentifikatsiya ───────────────────────────────────────────────────
def is_admin(user_id: int) -> bool:
    """config.py dagi admin yoki parol kiritgan admin."""
    return user_id in ADMIN_IDS or user_id in _authed_admins


def auth_admin(user_id: int) -> None:
    _authed_admins.add(user_id)
    _failed_attempts.pop(user_id, None)


def deauth_admin(user_id: int) -> None:
    _authed_admins.discard(user_id)


def get_attempts(user_id: int) -> int:
    return _failed_attempts.get(user_id, 0)


def inc_attempts(user_id: int) -> int:
    _failed_attempts[user_id] = _failed_attempts.get(user_id, 0) + 1
    return _failed_attempts[user_id]


def reset_attempts(user_id: int) -> None:
    _failed_attempts.pop(user_id, None)


def is_locked(user_id: int) -> bool:
    return _failed_attempts.get(user_id, 0) >= MAX_ATTEMPTS


# ─── Xabar o'chirish ─────────────────────────────────────────────────────────
async def delete_msg(message) -> None:
    """Xabarni xavfsiz o'chiradi."""
    try:
        await message.delete()
    except Exception:
        pass


async def delete_by_id(bot: Bot, chat_id: int, message_id: int) -> None:
    """ID bo'yicha xabarni xavfsiz o'chiradi."""
    try:
        await bot.delete_message(chat_id, message_id)
    except Exception:
        pass


# ─── Panel xabar menejeri ─────────────────────────────────────────────────────
async def show_panel(
    bot: Bot,
    chat_id: int,
    user_id: int,
    text: str,
    markup=None,
    parse_mode: str = "HTML",
) -> int:
    """
    Foydalanuvchi uchun mavjud panel xabarini tahrirlaydi.
    Agar xabar topilmasa yoki tahrirlab bo'lmasa — yangi yuboradi.
    Qaytariladigan qiymat: yangi/tahrirlangan xabarning message_id si.
    """
    old_id = _panel.get(user_id)
    if old_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=old_id,
                text=text,
                reply_markup=markup,
                parse_mode=parse_mode,
            )
            return old_id
        except Exception:
            pass  # tahrirlash imkonsiz → yangi yuboramiz

    sent = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=markup,
        parse_mode=parse_mode,
    )
    _panel[user_id] = sent.message_id
    return sent.message_id


def clear_panel(user_id: int) -> None:
    _panel.pop(user_id, None)


# ─── Obuna tekshiruvi ─────────────────────────────────────────────────────────
async def check_subscription(bot: Bot, user_id: int) -> list[dict]:
    """
    Foydalanuvchi a'zo bo'lmagan kanallar ro'yxatini qaytaradi.
    Agar bo'sh ro'yxat qaytsa — foydalanuvchi hamma kanallarga obuna.
    """
    channels = await db.get_required_channels()
    not_subbed: list[dict] = []
    for ch in channels:
        try:
            member = await bot.get_chat_member(ch["channel_id"], user_id)
            if member.status in ("left", "kicked", "banned"):
                not_subbed.append(ch)
        except Exception:
            # Kanalga kirish imkoni yo'q yoki foydalanuvchi yo'q
            not_subbed.append(ch)
    return not_subbed
