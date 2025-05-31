import threading
import sqlite3
import os
import datetime

# Flat structure: no package prefix needed for imports.

class SharedMemory:
    def __init__(self, db_path=None):
        self.lock = threading.Lock()
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'shared_memory.db')
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                file_format TEXT,
                timestamp TEXT,
                intent TEXT,
                extracted_fields TEXT,
                flags TEXT,
                thread_id TEXT
            )''')
            conn.commit()

    def log(self, entry: dict):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''INSERT INTO memory (source, file_format, timestamp, intent, extracted_fields, flags, thread_id)
                         VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                entry.get('source'),
                entry.get('file_format'),
                entry.get('timestamp', datetime.datetime.now().isoformat()),
                entry.get('intent'),
                str(entry.get('extracted_fields')) if entry.get('extracted_fields') else None,
                str(entry.get('flags')) if entry.get('flags') else None,
                entry.get('thread_id')
            ))
            conn.commit()

    def snapshot(self):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT source, file_format, timestamp, intent, extracted_fields, flags, thread_id FROM memory')
            rows = c.fetchall()
            keys = ['source', 'file_format', 'timestamp', 'intent', 'extracted_fields', 'flags', 'thread_id']
            return [dict(zip(keys, row)) for row in rows] 