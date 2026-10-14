from dataclasses import dataclass

from src.core.database import Database

from src.repositories.npc_repository import NPCRepository

from src.domain.world.repositories.world_repository import (
    WorldRepository,
)
from src.domain.world.repositories.region_repository import (
    RegionRepository,
)
from src.domain.world.repositories.location_repository import (
    LocationRepository,
)
from src.domain.world.repositories.faction_repository import (
    FactionRepository,
)

from src.domain.campaign.repositories.campaign_repository import (
    CampaignRepository,
)
from src.domain.campaign.repositories.campaign_region_repository import (
    CampaignRegionRepository,
)
from src.domain.campaign.repositories.campaign_location_repository import (
    CampaignLocationRepository,
)
from src.domain.campaign.repositories.campaign_faction_repository import (
    CampaignFactionRepository,
)

from src.domain.campaign.services.campaign_snapshot_service import (
    CampaignSnapshotService,
)


@dataclass(frozen=True)
class AppDependencies:
    npc_repository: NPCRepository

    world_repository: WorldRepository
    region_repository: RegionRepository
    location_repository: LocationRepository
    faction_repository: FactionRepository

    campaign_repository: CampaignRepository
    campaign_region_repository: CampaignRegionRepository
    campaign_location_repository: CampaignLocationRepository
    campaign_faction_repository: CampaignFactionRepository

    campaign_snapshot_service: CampaignSnapshotService


def build_dependencies(database: Database) -> AppDependencies:
    npc_repository = NPCRepository(database)

    world_repository = WorldRepository(database)
    region_repository = RegionRepository(database)
    location_repository = LocationRepository(database)
    faction_repository = FactionRepository(database)

    campaign_repository = CampaignRepository(database)
    campaign_region_repository = CampaignRegionRepository(database)
    campaign_location_repository = CampaignLocationRepository(database)
    campaign_faction_repository = CampaignFactionRepository(database)

    campaign_snapshot_service = CampaignSnapshotService(
        campaign_repository=campaign_repository,
        faction_repository=faction_repository,
        campaign_faction_repository=campaign_faction_repository,
        region_repository=region_repository,
        campaign_region_repository=campaign_region_repository,
        location_repository=location_repository,
        campaign_location_repository=campaign_location_repository,
    )

    return AppDependencies(
        npc_repository=npc_repository,
        world_repository=world_repository,
        region_repository=region_repository,
        location_repository=location_repository,
        faction_repository=faction_repository,
        campaign_repository=campaign_repository,
        campaign_region_repository=campaign_region_repository,
        campaign_location_repository=campaign_location_repository,
        campaign_faction_repository=campaign_faction_repository,
        campaign_snapshot_service=campaign_snapshot_service,
    )
