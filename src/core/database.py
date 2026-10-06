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
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS worlds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                world_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                region_type TEXT NOT NULL DEFAULT 'other',

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                region_id INTEGER NOT NULL,
                parent_location_id INTEGER,

                name TEXT NOT NULL,

                location_type TEXT NOT NULL DEFAULT 'other',

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                status TEXT NOT NULL DEFAULT 'planning',

                world_id INTEGER,

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS factions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                world_id INTEGER NOT NULL,

                name TEXT NOT NULL,

                faction_type TEXT NOT NULL
                    DEFAULT 'other',

                status TEXT NOT NULL
                    DEFAULT 'active',

                description TEXT NOT NULL
                    DEFAULT '',

                notes TEXT NOT NULL
                    DEFAULT '',

                created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP,

                updated_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS campaign_factions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                campaign_id INTEGER NOT NULL,
                source_faction_id INTEGER,

                name TEXT NOT NULL,
                faction_type TEXT NOT NULL DEFAULT 'other',
                status TEXT NOT NULL DEFAULT 'active',

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (
                    campaign_id,
                    source_faction_id
                )
            )
            """
        )
        
        self.connection.commit()
        
    def close(self):
        self.connection.close()