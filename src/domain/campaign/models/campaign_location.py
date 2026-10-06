from dataclasses import dataclass

from src.domain.world.models.location import (
    LocationType,
)


@dataclass
class CampaignLocation:
    campaign_id: int
    region_id: int
    name: str

    location_type: LocationType = LocationType.OTHER

    parent_location_id: int | None = None
    source_location_id: int | None = None

    description: str = ""
    notes: str = ""

    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None