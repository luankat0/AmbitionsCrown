from dataclasses import dataclass

from src.domain.world.models.region import (
    RegionType,
)


@dataclass
class CampaignRegion:
    campaign_id: int
    name: str
    
    region_type: RegionType = RegionType.OTHER
    
    source_region_id: int | None = None
    
    description: str = ""
    notes: str = ""
    
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None