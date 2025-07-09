import sqlite3

# Connect to SQLite DB (creates file if not present)
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Database initialized ✅")
