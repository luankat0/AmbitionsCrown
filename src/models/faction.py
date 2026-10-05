from dataclasses import dataclass
from enum import Enum


class FactionType(str, Enum):
    KINGDOM = "kingdom"
    GOVERNMENT = "government"
    GUILD = "guild"
    RELIGION = "religion"
    MILITARY = "military"
    CRIMINAL = "criminal"
    MERCHANT = "merchant"
    SECRET_SOCIETY = "secret_society"
    CULT = "cult"
    TRIBE = "tribe"
    OTHER = "other"


class FactionStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DESTROYED = "destroyed"
    HIDDEN = "hidden"


@dataclass
class Faction:
    world_id: int
    name: str

    faction_type: FactionType = (
        FactionType.OTHER
    )

    status: FactionStatus = (
        FactionStatus.ACTIVE
    )

    description: str = ""
    notes: str = ""

    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None