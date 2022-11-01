from databases import Database
from .db import DATABASE_URL


async def db_conn():
    async with Database(DATABASE_URL) as conn:
        yield conn
