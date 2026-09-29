from dataclasses import dataclass

@dataclass
class NPC:
    name: str
    race: str
    role: str
    region: str
    
    description: str = ""
    personality: str = ""
    notes: str = ""
    
    def get_summary(self):
            return f"{self.race} • {self.role} • {self.region}"