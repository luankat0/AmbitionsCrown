from dataclasses import dataclass

@dataclass
class World:
    name: str
    
    description: str = ""
    notes: str = ""
    
    id: int | None = None
    
    created_at: str | None = None
    updated_at: str | None = None
    
