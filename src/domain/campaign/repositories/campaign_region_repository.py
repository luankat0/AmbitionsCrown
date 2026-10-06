from src.domain.campaign.models.campaign_region import (
    CampaignRegion,
)

from src.domain.world.models.region import (
    RegionType,
)


class CampaignRegionRepository:
    def __init__(
        self,
        database
    ):
        self.database = database

    def add(
        self,
        region,
        commit=True
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            INSERT INTO campaign_regions (
                campaign_id,
                source_region_id,
                name,
                region_type,
                description,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                region.campaign_id,
                region.source_region_id,
                region.name,
                region.region_type.value,
                region.description,
                region.notes,
            )
        )
        
        if commit:
            self.database.connection.commit()

        region.id = cursor.lastrowid

        return region

    def get_by_id(
        self,
        region_id
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                source_region_id,
                name,
                region_type,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_regions
            WHERE id = ?
            """,
            (
                region_id,
            )
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_region(
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
                source_region_id,
                name,
                region_type,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_regions
            WHERE campaign_id = ?
            ORDER BY name
            """,
            (
                campaign_id,
            )
        )

        rows = cursor.fetchall()

        return [
            self._row_to_region(
                row
            )
            for row in rows
        ]

    def update(
        self,
        region
    ):
        if region.id is None:
            raise ValueError(
                "Não é possível atualizar uma região "
                "de campanha sem ID."
            )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE campaign_regions
            SET
                name = ?,
                region_type = ?,
                description = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                region.name,
                region.region_type.value,
                region.description,
                region.notes,
                region.id,
            )
        )

        self.database.connection.commit()

        return region

    def delete(
        self,
        region
    ):
        if region.id is None:
            raise ValueError(
                "Não é possível excluir uma região "
                "de campanha sem ID."
            )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            DELETE FROM campaign_regions
            WHERE id = ?
            """,
            (
                region.id,
            )
        )

        self.database.connection.commit()

    def _row_to_region(
        self,
        row
    ):
        return CampaignRegion(
            id=row["id"],
            campaign_id=row["campaign_id"],
            source_region_id=row["source_region_id"],
            name=row["name"],
            region_type=RegionType(
                row["region_type"]
            ),
            description=row["description"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )