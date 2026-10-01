from src.models.region import Region, RegionType

class RegionRepository:
    def __init__(self, database):
        self.database = database
        
    def add(self, region):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            INSERT INTO regions (
                world_id,
                name,
                region_type,
                description,
                notes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                region.world_id,
                region.name,
                region.region_type.value,
                region.description,
                region.notes
            )
        )
        
        self.database.connection.commit()
        
        region.id = cursor.lastrowid
        
    def get_all_by_world(
        self,
        world_id: int
    ):
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                world_id,
                name,
                region_type,
                description,
                notes,
                created_at,
                updated_at
            FROM regions
            WHERE world_id = ?
            ORDER BY id DESC
            """,
            (
                world_id,
            )
        )

        rows = cursor.fetchall()

        regions = []

        for row in rows:
            region = Region(
                id=row["id"],
                world_id=row["world_id"],
                name=row["name"],
                region_type=RegionType(
                    row["region_type"]
                ),
                description=row["description"],
                notes=row["notes"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

            regions.append(
                region
            )

        return regions

    def get_by_id(
        self,
        region_id: int
    ) -> Region | None:
        cursor = self.database.connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                world_id,
                name,
                region_type,
                description,
                notes,
                created_at,
                updated_at
            FROM regions
            WHERE id = ?
            """,
            (
                region_id,
            )
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Region(
            id=row["id"],
            world_id=row["world_id"],
            name=row["name"],
            region_type=RegionType(
                row["region_type"]
            ),
            description=row["description"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )