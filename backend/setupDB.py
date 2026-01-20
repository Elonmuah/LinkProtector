# setupDB.py
import sqlite3
import os

DATABASE = "analytics.db"

def create_tables():
    """Create all necessary tables if they don't exist"""
    if os.path.exists(DATABASE):
        print(f"Database '{DATABASE}' already exists. Tables will be created only if missing.")
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 1. Links / Tokens table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            token           TEXT PRIMARY KEY,
            original_url    TEXT NOT NULL,
            title           TEXT NOT NULL,
            tokenized_url   TEXT NOT NULL,
            created_at      TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            last_id         INTEGER
        )
    """)

    # 2. Raw clicks log (optional but useful for debugging/auditing)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clicks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            token       TEXT NOT NULL,
            click_time  TEXT NOT NULL DEFAULT (datetime('now', 'utc')),
            hour        INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
            FOREIGN KEY (token) REFERENCES links(token) ON DELETE CASCADE
        )
    """)

    # 3. Daily aggregated stats (fast queries for getDays)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            token       TEXT NOT NULL,
            date        TEXT NOT NULL,          -- '2026-01-15'
            total_clicks INTEGER DEFAULT 0,
            PRIMARY KEY (token, date),
            FOREIGN KEY (token) REFERENCES links(token) ON DELETE CASCADE
        )
    """)

    # 4. Hourly aggregated stats (fast queries for getHours)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hourly_stats (
            token       TEXT NOT NULL,
            date        TEXT NOT NULL,
            hour        INTEGER NOT NULL CHECK(hour BETWEEN 0 AND 23),
            clicks      INTEGER DEFAULT 0,
            PRIMARY KEY (token, date, hour),
            FOREIGN KEY (token) REFERENCES links(token) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print(f"Database '{DATABASE}' initialized successfully.")

if __name__ == "__main__":
    print("Running database setup...")
    create_tables()
    print("Setup complete.")