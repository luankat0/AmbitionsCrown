from src.models.npc import NPC

class NPCRepository:
    def __init__(self, database):
        self.database = database
        
    def add(self, npc):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            INSERT INTO npcs (
                name,
                race,
                role,
                region,
                description,
                personality,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                npc.name,
                npc.race,
                npc.role,
                npc.region,
                npc.description,
                npc.personality,
                npc.notes
            )
        )

        self.database.connection.commit()

        npc.id = cursor.lastrowid

        return npc
    
    def get_all(self):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                name,
                race,
                role,
                region,
                description,
                personality,
                notes,
                created_at
            FROM npcs
            ORDER BY id DESC
            """
        )

        rows = cursor.fetchall()

        npcs = []

        for row in rows:
            npc = NPC(
                id=row["id"],
                name=row["name"],
                race=row["race"],
                role=row["role"],
                region=row["region"],
                description=row["description"],
                personality=row["personality"],
                notes=row["notes"],
                created_at=row["created_at"]
            )

            npcs.append(npc)

        return npcs
    
    def update(self, npc):
        if npc.id is None:
            raise ValueError(
                "Não é possível atualizar um NPC sem ID."
            )
            
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            UPDATE npcs
            SET
                name = ?,
                race = ?,
                role = ?,
                region = ?,
                description = ?,
                personality = ?,
                notes = ?
            WHERE id = ?
            """,
            (
                npc.name,
                npc.race,
                npc.role,
                npc.region,
                npc.description,
                npc.personality,
                npc.notes,
                npc.id
            )
        )

        self.database.connection.commit()

        return npc
    
    def delete(self, npc):
        if npc.id is None:
            raise ValueError(
                "Não é possível excluir um NPC sem ID."
            )
        
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            DELETE FROM npcs
            WHERE id = ?
            """,
            (npc.id,)
        )
        
        self.database.connection.commit()