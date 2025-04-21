import sqlite3
from datetime import datetime

DB_PATH = 'videos.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            video_path TEXT,
            audio_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


def save_video_info(url, video_path, audio_path):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO videos (url, video_path, audio_path)           
        VALUES (?, ?, ?)
    """, (url, video_path, audio_path))

    conn.commit()
    conn.close()

def get_video_info(url):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT video_path, audio_path FROM videos WHERE url = ?', (url,))
    result = cursor.fetchone()
    conn.close()
    return result

