from dataclasses import dataclass

from src.domain.world.models.faction import (
    FactionStatus,
    FactionType
)

@dataclass
class CampaignFaction:
    campaign_id: int
    name: str
    
    faction_type: FactionType = FactionType.OTHER
    status: FactionStatus = FactionStatus.ACTIVE
    
    source_faction_id: int | None = None
    
    description: str = ""
    notes: str = ""
    
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None