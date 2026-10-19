from src.domain.campaign.models.campaign import Campaign, CampaignStatus

class CampaignRepository:
    def __init__(self, database):
        self.database = database
        
    def add(self, campaign):        
        if campaign.world_id is not None:
            existing_world = self.database.connection.execute(
                """ 
                SELECT 1
                FROM worlds
                WHERE id = ?
                LIMIT 1
                """,
                (campaign.world_id,)
            ).fetchone()
            
            if existing_world is None:
                raise ValueError(
                    "O mundo informado não existe."
                )
        
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
        
        # Consulta o estado persistido da Campaign
        cursor.execute(
            """ 
            SELECT world_id, snapshot_created_at
            FROM campaigns
            WHERE id = ?
            """,
            (campaign.id,)
        )
        
        persisted = cursor.fetchone()
        
        if persisted is None:
            raise ValueError(
                "A campanha informada não existe."
            )
        
        # O snapshot só pode ser marcado pelo método específico
        if (
            campaign.snapshot_created_at
            != persisted["snapshot_created_at"]
        ):
            raise ValueError(
                "Não é possível alterar o snapshot da campanha "
                "pelo método update()."
            )
        
        # Depois do snapshot, o World é imutável
        if (
            persisted["snapshot_created_at"] is not None
            and campaign.world_id != persisted["world_id"]
        ):
            raise ValueError(
                "Não é possível alterar o mundo de uma campanha "
                "após a criação do snapshot."
            )
        
        # O World informado precisa existir.
        if campaign.world_id is not None:
            cursor.execute(
                """ 
                SELECT 1
                FROM worlds
                WHERE id = ?
                LIMIT 1
                """,
                (campaign.world_id,)
            )
            
            if cursor.fetchone() is None:
                raise ValueError(
                    "O mundo informado não existe."
                )
        
        cursor.execute(
            """
            UPDATE campaigns
            SET
                name = ?,
                description = ?,
                notes = ?,
                status = ?,
                world_id = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                campaign.name,
                campaign.description,
                campaign.notes,
                campaign.status.value,
                campaign.world_id,
                campaign.id
            )
        )
        
        self.database.connection.commit()

        return campaign

    def mark_snapshot_created(
        self,
        campaign,
        commit=True
    ):
        if campaign.id is None:
            raise ValueError(
                "Não é possível marcar o snapshot "
                "de uma campanha sem ID."
            )
            
        cursor = self.database.connection.cursor()
        
        cursor.execute(
            """
            UPDATE campaigns
            SET
                snapshot_created_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (
                campaign.id,
            )
        )
        
        cursor.execute(
            """
            SELECT snapshot_created_at
            FROM campaigns
            WHERE id = ?
            """,
            (
                campaign.id,
            )
        )
        
        row = cursor.fetchone()
        
        if commit:
            self.database.connection.commit()
        
        if row is None:
            raise ValueError(
                "A campanha informada não existe."
            )
            
        campaign.snapshot_created_at = (
            row["snapshot_created_at"]
        )
        
        return campaign

