from dataclasses import dataclass
from enum import Enum

class RegionType(str, Enum):
    KINGDOM = "kingdom"
    PROVINCE = "province"
    TERRITORY = "territory"
    FOREST = "forest"
    DESERT = "desert"
    MOUNTAINS = "mountains"
    ISLAND = "island"
    OTHER = "other"
    
@dataclass
class Region:
    world_id: int
    name: str
    
    region_type: RegionType = RegionType.OTHER
    
    description: str = ""
    notes: str = ""
    
    id: int | None = None
    
    created_at: str | None = None
    updated_at: str | None = None