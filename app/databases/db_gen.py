import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    salt blob NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)
""")
cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", ("max", "pass123"))
cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", ("sophia", "secret"))
cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", ("sam", "geheim"))

conn.commit()
conn.close()

print("Database setup complete!")

