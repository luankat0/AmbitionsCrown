from src.domain.world.models.world import World

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
        
    def delete(
        self,
        world
    ):
        if world.id is None:
            raise ValueError(
                "Não é possível excluir "
                "um mundo sem ID."
            )
        
        cursor = (
            self.database
            .connection
            .cursor()
        )
        
        cursor.execute(
            """
            SELECT 1
            FROM regions
            WHERE world_id = ?
            LIMIT 1
            """,
            (
                world.id,
            )
        )
        
        has_regions = (
            cursor.fetchone()
            is not None
        )
        
        if has_regions:
            raise ValueError(
                "Não é possível excluir este mundo "
                "porque ele possui regiôes."
            )
        
        cursor.execute(
            """
            SELECT 1
            FROM campaigns
            WHERE world_id = ?
            LIMIT 1
            """,
            (
                world.id,
            )
        )
        
        is_used_by_campaign = (
            cursor.fetchone()
            is not None
        )
        
        if is_used_by_campaign:
            raise ValueError(
                "Não é possível excluir este mundo "
                "porque ele está sendo usado "
                "por uma campanha."
            )
        
        cursor.execute(
            """
            DELETE FROM worlds
            WHERE id = ?
            """,
            (
                world.id,
            )
        )
        
        self.database.connection.commit()


        
        if has_regions:
            raise ValueError(
                "Não é possível excluir este mundo "
                "porque ele possui regiões."
            )
        
        cursor.execute(
            """
            SELECT 1
            FROM campaigns
            WHERE world_id = ?
            LIMIT 1
            """,
            (
                world.id,
            )
        )
        
        is_used_by_campaign = (
            cursor.fetchone()
            is not None
        )
        
        if is_used_by_campaign:
            raise ValueError(
                "Não é possível excluir este mundo "
                "porque ele está sendo usado "
                "por uma campanha."
            )
        
        cursor.execute(
            """
            DELETE FROM worlds
            WHERE id = ?
            """,
            (
                world.id,
            )
        )
        
        self.database.connection.commit()

