import json
import aiomysql
from config import MYSQL_CONFIG

async def insert_into_mysql():
    with open("pipeline/raw_data.json") as f:
        data = json.load(f)

    # Connect without selecting a DB first
    conn = await aiomysql.connect(
        host=MYSQL_CONFIG["host"],
        port=MYSQL_CONFIG["port"],
        user=MYSQL_CONFIG["user"],
        password=MYSQL_CONFIG["password"]
    )

    async with conn.cursor() as cur:
        # Create the database if it doesn't exist
        await cur.execute("CREATE DATABASE IF NOT EXISTS demo_db")
        await conn.select_db("demo_db")

        # Create the documents table
        await cur.execute("""CREATE TABLE IF NOT EXISTS documents (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title TEXT,
            doc_type VARCHAR(255),
            publication_date DATE
        )""")

        # Insert each document
        for doc in data:
            await cur.execute(
                "INSERT INTO documents (title, doc_type, publication_date) VALUES (%s, %s, %s)",
                (doc.get('title', ''), doc.get('document_type', ''), doc.get('publication_date', None))

            )

    await conn.commit()
    await conn.ensure_closed()
    print("Data inserted into MySQL database successfully.")
if __name__ == "__main__":
    import asyncio
    asyncio.run(insert_into_mysql())