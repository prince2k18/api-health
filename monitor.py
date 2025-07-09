import httpx
import aiosqlite
import time

DB = "db.sqlite3"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS apis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )""")
        await db.commit()

async def add_api(url):
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR IGNORE INTO apis (url) VALUES (?)", (url,))
        await db.commit()

async def check_all_apis():
    results = []
    async with aiosqlite.connect(DB) as db:
        async with db.execute("SELECT url FROM apis") as cursor:
            rows = await cursor.fetchall()
            for (url,) in rows:
                try:
                    start = time.time()
                    r = httpx.get(url, timeout=5)
                    latency = round((time.time() - start) * 1000)
                    results.append({
                        "url": url,
                        "status": r.status_code,
                        "latency": latency
                    })
                except:
                    results.append({
                        "url": url,
                        "status": "DOWN",
                        "latency": "N/A"
                    })
    return results
