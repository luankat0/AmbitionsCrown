from src.models.location import Location, LocationType

class LocationRepository:
    def __init__(self, database):
        self.database = database
        
    def add(self, location):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            INSERT INTO locations (
                region_id,
                parent_location_id,
                name,
                location_type,
                description,
                notes
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                location.region_id,
                location.parent_location_id,
                location.name,
                location.location_type.value,
                location.description,
                location.notes
            )
        )
        
        self.database.connection.commit()
        
        location.id = cursor.lastrowid
        
        return location
    
    def get_by_id(
        self,
        location_id: int
    ) -> Location | None:
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            SELECT
                id,
                region_id,
                parent_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM locations
            WHERE id = ?
            """,
            (
                location_id,
            )
        )
        
        row = cursor.fetchone()
        
        if row is None:
            return None
        
        return Location(
            id=row["id"],
            region_id=row["region_id"],
            parent_location_id=(
                row["parent_location_id"]
            ),
            name=row["name"],
            location_type=LocationType(
                row["location_type"]
            ),
            description=row["description"],
            notes=row["notes"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )
        
    def get_all_by_region(
        self,
        region_id: int
    ):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            SELECT
                id,
                region_id,
                parent_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM locations
            WHERE region_id = ?
            ORDER BY id DESC
            """,
            (
                region_id,
            )
        )

        rows = cursor.fetchall()
        
        locations = []
        
        for row in rows:
            location = Location(
                id=row["id"],
                region_id=row["region_id"],
                parent_location_id=(
                    row["parent_location_id"]
                ),
                name=row["name"],
                location_type=LocationType(
                    row["location_type"]
                ),
                description=row["description"],
                notes=row["notes"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            
            locations.append(
                location
            )
            
        return locations

    def get_children(
        self,
        parent_location_id: int
    ):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            SELECT
                id,
                region_id,
                parent_location_id,
                name,
                location_type,
                description,
                notes,
                created_at,
                updated_at
            FROM locations
            WHERE parent_location_id = ?
            ORDER BY id DESC
            """,
            (
                parent_location_id,
            )
        )
        
        rows = cursor.fetchall()
        
        locations = []
        
        for row in rows:
            location = Location(
                id=row["id"],
                region_id=row["region_id"],
                parent_location_id=(
                    row["parent_location_id"]
                ),
                name=row["name"],
                location_type=LocationType(
                    row["location_type"]
                ),
                description=row["description"],
                notes=row["notes"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )

            locations.append(
                location
            )

        return locations