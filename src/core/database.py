import sqlite3

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "ambitions_crown.db"

class Database:
    def __init__(
        self,
        database_path: str | Path = DATABASE_PATH
    ):
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(
                parents=True,
                exist_ok=True
            )
        
        self.connection = sqlite3.connect(
            database_path
        )
        
        self.connection.row_factory = sqlite3.Row
        
        # Ativa a integridade referencial para esta conexão SQLite
        self.connection.execute(
            "PRAGMA foreign_keys = ON"
        )
    
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

                snapshot_created_at TEXT,
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
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS campaign_regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                campaign_id INTEGER NOT NULL,
                source_region_id INTEGER,

                name TEXT NOT NULL,
                region_type TEXT NOT NULL DEFAULT 'other',

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (
                    campaign_id,
                    source_region_id
                )
            )
            """
        )
        
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS campaign_locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                campaign_id INTEGER NOT NULL,
                region_id INTEGER NOT NULL,

                parent_location_id INTEGER,
                source_location_id INTEGER,

                name TEXT NOT NULL,
                location_type TEXT NOT NULL DEFAULT 'other',

                description TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',

                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

                UNIQUE (
                    campaign_id,
                    source_location_id
                )
            )
            """
        )
        
        self.connection.commit()
     
    def get_schema_version(self) -> int:
        """
        Retorna a versão atual do esquema SQLite.

        Não executa migrations e não modifica
        o banco de dados.
        """

        row = self.connection.execute(
            "PRAGMA user_version"
        ).fetchone()

        if row is None:
            raise RuntimeError(
                "Não foi possível consultar "
                "a versão do esquema SQLite."
            )

        return int(row[0])
     
    def backup_to(
        self,
        destination_path: str | Path
    ) -> Path:
        """
        Cria um backup consistente do SQLite.

        Não sobrescreve arquivos existentes.
        Não modifica o banco original.
        """

        if self.connection.in_transaction:
            raise RuntimeError(
                "Finalize a transação antes "
                "de criar o backup."
            )

        destination = Path(destination_path)

        destination.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Reserva o caminho sem sobrescrever
        # um backup já existente.
        with destination.open("xb"):
            pass

        try:
            backup_connection = sqlite3.connect(
                destination
            )

            try:
                self.connection.backup(
                    backup_connection
                )

            finally:
                backup_connection.close()

        except Exception:
            # Remove somente o arquivo reservado
            # por esta chamada, se o backup falhar.
            destination.unlink(missing_ok=True)
            raise

        return destination 
        
    def close(self):
        self.connection.close()
