from src.domain.campaign.models.campaign_location import (
    CampaignLocation,
)

from src.domain.world.models.location import (
    LocationType,
)


class CampaignLocationRepository:
    def __init__(
        self,
        database
    ):
        self.database = database

    def add(
        self,
        location
    ):
        self._validate_parent(
            location
        )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            INSERT INTO campaign_locations (
                campaign_id,
                region_id,
                parent_location_id,
                source_location_id,
                name,
                location_type,
                description,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                location.campaign_id,
                location.region_id,
                location.parent_location_id,
                location.source_location_id,
                location.name,
                location.location_type.value,
                location.description,
                location.notes,
            )
        )

        self.database.connection.commit()

        location.id = cursor.lastrowid

        return location

    def get_by_id(
        self,
        location_id
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                region_id,
                parent_location_id,
                source_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_locations
            WHERE id = ?
            """,
            (
                location_id,
            )
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_location(
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
                region_id,
                parent_location_id,
                source_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_locations
            WHERE campaign_id = ?
            ORDER BY name
            """,
            (
                campaign_id,
            )
        )

        rows = cursor.fetchall()

        return [
            self._row_to_location(
                row
            )
            for row in rows
        ]

    def get_all_by_region(
        self,
        region_id
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                region_id,
                parent_location_id,
                source_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_locations
            WHERE region_id = ?
            ORDER BY name
            """,
            (
                region_id,
            )
        )

        rows = cursor.fetchall()

        return [
            self._row_to_location(
                row
            )
            for row in rows
        ]

    def get_children(
        self,
        parent_location_id
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                campaign_id,
                region_id,
                parent_location_id,
                source_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM campaign_locations
            WHERE parent_location_id = ?
            ORDER BY name
            """,
            (
                parent_location_id,
            )
        )

        rows = cursor.fetchall()

        return [
            self._row_to_location(
                row
            )
            for row in rows
        ]

    def update(
        self,
        location
    ):
        if location.id is None:
            raise ValueError(
                "Não é possível atualizar um local "
                "de campanha sem ID."
            )

        self._validate_parent(
            location
        )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            UPDATE campaign_locations
            SET
                name = ?,
                location_type = ?,
                description = ?,
                notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                location.name,
                location.location_type.value,
                location.description,
                location.notes,
                location.id,
            )
        )

        self.database.connection.commit()

        return location

    def delete(
        self,
        location
    ):
        if location.id is None:
            raise ValueError(
                "Não é possível excluir um local "
                "de campanha sem ID."
            )

        children = self.get_children(
            location.id
        )

        if children:
            raise ValueError(
                "Não é possível excluir este local "
                "porque ele possui sublocais."
            )

        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            DELETE FROM campaign_locations
            WHERE id = ?
            """,
            (
                location.id,
            )
        )

        self.database.connection.commit()

    def _validate_parent(
        self,
        location
    ):
        parent_id = (
            location.parent_location_id
        )

        if parent_id is None:
            return

        if (
            location.id is not None
            and parent_id == location.id
        ):
            raise ValueError(
                "Um local não pode ser pai de si mesmo."
            )

        parent = self.get_by_id(
            parent_id
        )

        if parent is None:
            raise ValueError(
                "O local pai informado não existe."
            )

        if (
            parent.campaign_id
            != location.campaign_id
        ):
            raise ValueError(
                "O local pai deve pertencer "
                "à mesma campanha."
            )

        if (
            parent.region_id
            != location.region_id
        ):
            raise ValueError(
                "O local pai deve pertencer "
                "à mesma região."
            )

    def _row_to_location(
        self,
        row
    ):
        return CampaignLocation(
            id=row["id"],
            campaign_id=row["campaign_id"],
            region_id=row["region_id"],
            parent_location_id=row[
                "parent_location_id"
            ],
            source_location_id=row[
                "source_location_id"
            ],
            name=row["name"],
            location_type=LocationType(
                row["location_type"]
            ),
            description=row["description"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )