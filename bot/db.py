import pathlib
import aiosqlite
from typing import Final

# /data/bot.db находится на один уровень выше /bot
DB_PATH: Final = (
    pathlib.Path(__file__).resolve().parent.parent / "data" / "bot.db"
)


async def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                consent INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        await db.commit()


async def set_consent(user_id: int, consent: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            INSERT INTO users(user_id, consent)
            VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET consent = excluded.consent;
            """,
            (user_id, 1 if consent else 0)
        )
        await db.commit()


async def has_consent(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT consent FROM users WHERE user_id = ?",
            (user_id,)
        ) as c:
            row = await c.fetchone()

    if row is None:
        return False

    return bool(row[0])
