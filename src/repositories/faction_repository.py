from src.models.faction import (
    Faction,
    FactionStatus,
    FactionType,
)


class FactionRepository:
    def __init__(
        self,
        database
    ):
        self.database = database

    def add(
        self,
        faction
    ):
        cursor = (
            self.database
            .connection
            .cursor()
        )

        cursor.execute(
            """
            INSERT INTO factions (
                world_id,
                name,
                faction_type,
                status,
                description,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                faction.world_id,
                faction.name,
                faction.faction_type.value,
                faction.status.value,
                faction.description,
                faction.notes,
            )
        )

        self.database.connection.commit()

        faction.id = cursor.lastrowid

        return faction

    def get_by_id(
        self,
        faction_id
    ):
        cursor = (
            self.database
            .connection
            .cursor()
        )

        cursor.execute(
            """
            SELECT
                id,
                world_id,
                name,
                faction_type,
                status,
                description,
                notes,
                created_at,
                updated_at
            FROM factions
            WHERE id = ?
            """,
            (
                faction_id,
            )
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_faction(
            row
        )

    def get_all_by_world(
        self,
        world_id
    ):
        cursor = (
            self.database
            .connection
            .cursor()
        )

        cursor.execute(
            """
            SELECT
                id,
                world_id,
                name,
                faction_type,
                status,
                description,
                notes,
                created_at,
                updated_at
            FROM factions
            WHERE world_id = ?
            ORDER BY name
            """,
            (
                world_id,
            )
        )

        rows = cursor.fetchall()

        return [
            self._row_to_faction(row)
            for row in rows
        ]

    def _row_to_faction(
        self,
        row
    ):
        return Faction(
            id=row["id"],
            world_id=row["world_id"],
            name=row["name"],
            faction_type=FactionType(
                row["faction_type"]
            ),
            status=FactionStatus(
                row["status"]
            ),
            description=row["description"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )
        
    def update(self, faction):
        if faction.id is None:
            raise ValueError(
                "Não é possível atualizar uma facção sem ID."
            )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE factions
            SET
                name = ?,
                faction_type = ?,
                status = ?,
                description = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                faction.name,
                faction.faction_type.value,
                faction.status.value,
                faction.description,
                faction.notes,
                faction.id,
            )
        )

        self.database.connection.commit()

        return faction

