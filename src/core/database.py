import sqlite3

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "ambitions_crown.db"

class Database:
    def __init__(self):
        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True
        )
        
        self.connection = sqlite3.connect(
            DATABASE_PATH
        )
        
        self.connection.row_factory = sqlite3.Row
    
    def create_tables(self):
        cursor = self.connection.cursor()
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS npcs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                race TEXT NOT NULL DEFAULT '',
                role TEXT NOT NULL DEFAULT '',
                region TEXT NOT NULL DEFAULT '',
                description TEXT NOT NULL DEFAULT '',
                personality TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        self.connection.commit()
        
    def close(self):
        self.connection.close()