import aiosqlite
from config import DATABASE_PATH, DEFAULT_ADMIN_PASSWORD


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript("""
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER UNIQUE,
                username   TEXT,
                full_name  TEXT,
                language   TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS categories (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name_uz    TEXT NOT NULL,
                name_ru    TEXT NOT NULL,
                name_en    TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS files (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id    INTEGER NOT NULL,
                name_uz        TEXT NOT NULL,
                name_ru        TEXT NOT NULL,
                name_en        TEXT NOT NULL,
                file_id        TEXT NOT NULL,
                file_type      TEXT NOT NULL,
                download_count INTEGER DEFAULT 0,
                created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS downloads (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL,
                file_id       INTEGER NOT NULL,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS bot_settings (
                key   TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS required_channels (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id TEXT NOT NULL UNIQUE,
                title      TEXT NOT NULL,
                url        TEXT NOT NULL
            );
        """)
        await db.execute(
            "INSERT OR IGNORE INTO bot_settings (key, value) VALUES ('admin_password', ?)",
            (DEFAULT_ADMIN_PASSWORD,)
        )
        await db.commit()


# ─── USERS ───────────────────────────────────────────────────────
async def add_or_update_user(user_id: int, username: str, full_name: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                username  = excluded.username,
                full_name = excluded.full_name
        """, (user_id, username, full_name))
        await db.commit()


async def get_user_language(user_id: int):
    """None qaytaradi agar til hali tanlanmagan bo'lsa."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else None


async def set_user_language(user_id: int, lang: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id)
        )
        await db.commit()


async def get_total_users() -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


async def get_new_users_today() -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT COUNT(*) FROM users WHERE DATE(created_at) = DATE('now')"
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else 0


# ─── CATEGORIES ──────────────────────────────────────────────────
async def add_category(name_uz: str, name_ru: str, name_en: str) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            "INSERT INTO categories (name_uz, name_ru, name_en) VALUES (?, ?, ?)",
            (name_uz, name_ru, name_en)
        )
        await db.commit()
        return cur.lastrowid


async def get_all_categories() -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, name_uz, name_ru, name_en FROM categories ORDER BY id"
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_category_by_id(cat_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM categories WHERE id = ?", (cat_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def delete_category(cat_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
        await db.commit()


# ─── FILES ───────────────────────────────────────────────────────
async def add_file(
    category_id: int,
    name_uz: str, name_ru: str, name_en: str,
    file_id: str, file_type: str,
) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute("""
            INSERT INTO files (category_id, name_uz, name_ru, name_en, file_id, file_type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (category_id, name_uz, name_ru, name_en, file_id, file_type))
        await db.commit()
        return cur.lastrowid


async def get_files_by_category(category_id: int) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM files WHERE category_id = ? ORDER BY id",
            (category_id,)
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_file_by_id(file_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM files WHERE id = ?", (file_id,)
        ) as cur:
            row = await cur.fetchone()
            return dict(row) if row else None


async def delete_file(file_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM files WHERE id = ?", (file_id,))
        await db.commit()


async def increment_download(file_id: int, user_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE files SET download_count = download_count + 1 WHERE id = ?",
            (file_id,)
        )
        await db.execute(
            "INSERT INTO downloads (user_id, file_id) VALUES (?, ?)",
            (user_id, file_id)
        )
        await db.commit()


async def get_total_downloads() -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute("SELECT SUM(download_count) FROM files") as cur:
            row = await cur.fetchone()
            return row[0] or 0


async def get_top_files(limit: int = 5) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT name_uz, name_ru, name_en, download_count
            FROM files ORDER BY download_count DESC LIMIT ?
        """, (limit,)) as cur:
            return [dict(r) for r in await cur.fetchall()]


# ─── BOT SETTINGS ────────────────────────────────────────────────
async def get_admin_password() -> str:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT value FROM bot_settings WHERE key = 'admin_password'"
        ) as cur:
            row = await cur.fetchone()
            return row[0] if row else DEFAULT_ADMIN_PASSWORD


async def set_admin_password(new_password: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO bot_settings (key, value) VALUES ('admin_password', ?)",
            (new_password,)
        )
        await db.commit()


# ─── REQUIRED CHANNELS ───────────────────────────────────────────
async def get_required_channels() -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, channel_id, title, url FROM required_channels ORDER BY id"
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def add_required_channel(channel_id: str, title: str, url: str):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO required_channels (channel_id, title, url) VALUES (?, ?, ?)",
            (channel_id, title, url)
        )
        await db.commit()


async def delete_required_channel(row_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM required_channels WHERE id = ?", (row_id,))
        await db.commit()
