from src.domain.campaign.models.campaign_faction import (
    CampaignFaction,
)

from src.domain.world.models.faction import (
    FactionStatus,
    FactionType,
)


class CampaignFactionRepository:
    def __init__(self, database):
        self.database = database

    def add(
        self,
        faction,
        commit=True
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            INSERT INTO campaign_factions (
                campaign_id,
                source_faction_id,
                name,
                faction_type,
                status,
                description,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                faction.campaign_id,
                faction.source_faction_id,
                faction.name,
                faction.faction_type.value,
                faction.status.value,
                faction.description,
                faction.notes,
            )
        )
        if commit:
            self.database.connection.commit()

        faction.id = cursor.lastrowid

        return faction

    def get_by_id(
        self,
        faction_id
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                source_faction_id,
                name,
                faction_type,
                status,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_factions
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

    def get_all_by_campaign(
        self,
        campaign_id
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                source_faction_id,
                name,
                faction_type,
                status,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_factions
            WHERE campaign_id = ?
            ORDER BY name
            """,
            (
                campaign_id,
            )
        )

        rows = cursor.fetchall()

        return [
            self._row_to_faction(
                row
            )
            for row in rows
        ]

    def _row_to_faction(
        self,
        row
    ):
        return CampaignFaction(
            id=row["id"],
            campaign_id=row["campaign_id"],
            source_faction_id=row["source_faction_id"],
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

    def update(
        self,
        faction
    ):
        if faction.id is None:
            raise ValueError(
                "Não é possível atualizar uma facção "
                "de campanha sem ID."
            )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE campaign_factions
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
    
    def delete(
        self,
        faction
    ):
        if faction.id is None:
            raise ValueError(
                "Não é possível excluir uma facção "
                "de campanha sem ID."
            )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            DELETE FROM campaign_factions
            WHERE id = ?
            """,
            (
                faction.id,
            )
        )

        self.database.connection.commit()

