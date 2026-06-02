import sqlite3

db = sqlite3.connect("movies.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies(
    code TEXT PRIMARY KEY,
    name TEXT,
    info TEXT,
    file_id TEXT
)
""")

db.commit()


def add_movie(code, name, info, file_id):
    cursor.execute(
        "INSERT OR REPLACE INTO movies VALUES (?, ?, ?, ?)",
        (code, name, info, file_id)
    )
    db.commit()


def get_movie(code):
    cursor.execute(
        "SELECT * FROM movies WHERE code=?",
        (code,)
    )
    return cursor.fetchone()
