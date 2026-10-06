from src.domain.campaign.models.campaign_faction import (
    CampaignFaction,
)

from src.domain.campaign.models.campaign_region import (
    CampaignRegion,
)


class CampaignSnapshotService:
    def __init__(
        self,
        faction_repository,
        campaign_faction_repository,
        region_repository,
        campaign_region_repository
    ):
        self.faction_repository = (
            faction_repository
        )
        
        self.campaign_faction_repository = (
            campaign_faction_repository
        )
        
        self.region_repository = (
            region_repository
        )
        
        self.campaign_region_repository = (
            campaign_region_repository
        )
        
    def snapshot_factions(
        self,
        campaign
    ):
        if campaign.id is None:
            raise ValueError(
                "Não é possível criar snapshot "
                "de uma campanha sem ID."
            )
            
        if campaign.world_id is None:
            return []
        
        world_factions = (
            self.faction_repository
            .get_all_by_world(
                campaign.world_id
            )
        )
        
        campaign_factions = (
            self.campaign_faction_repository
            .get_all_by_campaign(
                campaign.id
            )
        )
        
        existing_source_ids = (
            faction.source_faction_id
            for faction in campaign_factions
            if faction.source_faction_id is not None
        )
        
        created_factions = []
        
        for world_faction in world_factions:
            if world_faction.id in existing_source_ids:
                continue
            
            campaign_faction = CampaignFaction(
                campaign_id=campaign.id,
                source_faction_id=world_faction.id,
                name=world_faction.name,
                faction_type=world_faction.faction_type,
                status=world_faction.status,
                description=world_faction.description,
                notes=world_faction.notes,
            )
            
            self.campaign_faction_repository.add(
                campaign_faction
            )
            
            created_factions.append(
                campaign_faction
            )
            
        return created_factions
    
    def snapshot_regions(
        self,
        campaign
    ):
        if campaign.id is None:
            raise ValueError(
                "Não é possível criar snapshot "
                "de uma campanha sem ID."
            )
        
        if campaign.world_id is None:
            return []
        
        world_regions = (
            self.region_repository
            .get_all_by_world(
                campaign.world_id
            )
        )
        
        campaign_regions = (
            self.campaign_region_repository
            .get_all_by_campaign(
                campaign.id
            )
        )
        
        existing_source_ids = {
            region.source_region_id
            for region in campaign_regions
            if region.source_region_id is not None
        }
        
        created_regions = []
        
        for world_region in world_regions:
            if world_region.id in existing_source_ids:
                continue
            
            campaign_region = CampaignRegion(
                campaign_id=campaign.id,
                source_region_id=world_region.id,
                name=world_region.name,
                region_type=world_region.region_type,
                description=world_region.description,
                notes=world_region.notes,
            )
            
            self.campaign_region_repository.add(
                campaign_region
            )
            
            created_regions.append(
                campaign_region
            )
        
        return created_regions