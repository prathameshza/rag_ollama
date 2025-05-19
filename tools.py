import aiomysql
from pipeline.config import MYSQL_CONFIG

async def search_documents(keyword: str) -> list:
    conn = await aiomysql.connect(**MYSQL_CONFIG)
    async with conn.cursor() as cur:
        await cur.execute(
            "SELECT title FROM documents WHERE title LIKE %s ORDER BY publication_date DESC LIMIT 5",
            (f"%{keyword}%",)
        )
        results = await cur.fetchall()
    await conn.ensure_closed()
    return [r[0] for r in results]
