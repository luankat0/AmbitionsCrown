from dataclasses import dataclass
from enum import Enum

class LocationType(str, Enum):
    CITY = "city"
    VILLAGE = "village"
    CAPITAL = "capital"
    DISTRICT = "district"
    FORTRESS = "fortress"
    CASTLE = "castle"
    TOWER = "tower"
    DUNGEON = "dungeon"
    TEMPLE = "temple"
    RUIN = "ruin"
    TAVERN = "tavern"
    CAMP = "camp"
    LANDMARK = "landmark"
    OTHER = "other"
    
@dataclass
class Location:
    region_id: int
    name: str
    
    location_type: LocationType = LocationType.OTHER
    
    parent_location_id: int | None = None
    
    description: str = ""
    notes: str = ""
    
    id: int | None = None
    
    created_at: str | None = None
    updated_at: str | None = None
    
