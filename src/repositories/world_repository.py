from src.models.world import World

class WorldRepository:
    def __init__(self, database):
        self.database = database
        
    def add(self, world):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            INSERT INTO worlds (
                name,
                description,
                notes
            )
            VALUES (?, ?, ?)
            """,
            (
                world.name,
                world.description,
                world.notes
            )
        )
        
        self.database.connection.commit()
        
        world.id = cursor.lastrowid
        
        return world
    
    def get_all(self):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            SELECT
                id,
                name,
                description,
                notes,
                created_at,
                updated_at
            FROM worlds
            ORDER BY id DESC
            """
        )
        
        rows = cursor.fetchall()
        
        worlds = []
        
        for row in rows:
            world = World(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                notes=row["notes"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            
            worlds.append(
                world
            )
            
        return worlds
    
    def get_by_id(
        self, 
        world_id: int
    ) -> World | None:
        
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            SELECT
                id,
                name,
                description,
                notes,
                created_at,
                updated_at
            FROM worlds
            WHERE id = ?
            """,
            (
                world_id,
            )
        )
        
        row = cursor.fetchone()
            
        if row is None:
            return None
                
        return World(
            id=row["id"],
            name=row["name"],
            description=row["description"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
        
