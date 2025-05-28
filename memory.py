import sqlite3
from datetime import datetime

class Memory:
    """
    Shared Memory module using SQLite to store logs of processed inputs.
    """
    def __init__(self, db_path="memory.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT,
                input_format TEXT,
                intent TEXT,
                timestamp TEXT,
                extracted TEXT,
                thread_id TEXT
            )
        ''')
        self.conn.commit()

    def log(self, source, input_format, intent, extracted, thread_id, timestamp=None):
        if not timestamp:
            timestamp = datetime.now().isoformat()
        c = self.conn.cursor()
        c.execute('''
            INSERT INTO memory (source, input_format, intent, timestamp, extracted, thread_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (source, input_format, intent, timestamp, extracted, thread_id))
        self.conn.commit()

    def fetch_all(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM memory')
        return c.fetchall()
