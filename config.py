import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8634905349:AAGQQtNGLbaIImX1O3gZrKd-fMJPsKu6nMc")

# config.py da boshlang'ich adminlar (har doim admin, parolsiz)
ADMIN_IDS: list[int] = [6917065134]

DATABASE_PATH: str = "library.db"

# Birinchi ishga tushirilganda ishlatiladigan parol.
# Admin paneldan o'zgartirilgandan keyin DB dagi parol ishlatiladi.
DEFAULT_ADMIN_PASSWORD: str = "admin1234"
