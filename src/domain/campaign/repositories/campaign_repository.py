from src.domain.campaign.models.campaign import Campaign, CampaignStatus

class CampaignRepository:
    def __init__(self, database):
        self.database = database
        
    def add(self, campaign):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            INSERT INTO campaigns (
                name,
                description,
                notes,
                status,
                world_id,
                snapshot_created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                campaign.name,
                campaign.description,
                campaign.notes,
                campaign.status.value,
                campaign.world_id,
                campaign.snapshot_created_at
            )
        )
        
        self.database.connection.commit()
        
        campaign.id = cursor.lastrowid
        
        return campaign
    
    def get_all(self):
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            SELECT
                id,
                name,
                description,
                notes,
                status,
                world_id,
                snapshot_created_at,
                created_at,
                updated_at
            FROM campaigns
            ORDER BY id DESC
            """
        )
        
        rows = cursor.fetchall()
        
        campaigns = []
        
        for row in rows:
            campaign = Campaign(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                notes=row["notes"],
                status=CampaignStatus(
                    row["status"]
                ),
                world_id=row["world_id"],
                snapshot_created_at=row[
                    "snapshot_created_at"
                ],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            
            campaigns.append(
                campaign
            )
            
        return campaigns
    
    def update(self, campaign):
        if campaign.id is None:
            raise ValueError(
                "Não é possível atualizar uma campanha sem ID."
            )
            
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            UPDATE campaigns
            SET
                name = ?,
                description = ?,
                notes = ?,
                status = ?,
                world_id = ?,
                snapshot_created_at = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                campaign.name,
                campaign.description,
                campaign.notes,
                campaign.status.value,
                campaign.world_id,
                campaign.snapshot_created_at,
                campaign.id
            )
        )
        
        self.database.connection.commit()

        return campaign
