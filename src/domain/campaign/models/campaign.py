from dataclasses import dataclass
from enum import Enum

class CampaignStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    PAUSED = "paused"
    FINISHED = "finished"
    ARCHIVED = "archived"
    
@dataclass
class Campaign:
    name: str
    
    description: str = ""
    notes: str = ""
    
    status: CampaignStatus = CampaignStatus.PLANNING
    
    world_id: int | None = None
    
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    snapshot_created_at: str | None = None