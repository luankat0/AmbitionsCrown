from src.domain.campaign.models.campaign_faction import (
    CampaignFaction,
)

from src.domain.campaign.models.campaign_region import (
    CampaignRegion,
)

from src.domain.campaign.models.campaign_location import (
    CampaignLocation,
)


class CampaignSnapshotService:
    def __init__(
        self,
        campaign_repository,
        faction_repository,
        campaign_faction_repository,
        region_repository,
        campaign_region_repository,
        location_repository,
        campaign_location_repository
    ):
        self.campaign_repository = (
            campaign_repository
        )
        
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
        
        self.location_repository = (
            location_repository
        )
        
        self.campaign_location_repository = (
            campaign_location_repository
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
    
    def snapshot_locations(
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
        
        campaign_regions = (
            self.campaign_region_repository
            .get_all_by_campaign(
                campaign.id
            )
        )
        
        region_id_map = {
            region.source_region_id: region.id
            for region in campaign_regions
            if (
                region.source_region_id is not None
                and region.id is not None
            )
        }
        
        world_regions = (
            self.region_repository
            .get_all_by_world(
                campaign.world_id
            )
        )
        
        campaign_locations = (
            self.campaign_location_repository
            .get_all_by_campaign(
                campaign.id
            )
        )
        
        location_id_map = {
            location.source_location_id: location.id
            for location in campaign_locations
            if (
                location.source_location_id is not None
                and location.id is not None
            )
        }
        
        pending_locations = []
        
        for world_region in world_regions:
            campaign_region_id = (
                region_id_map.get(
                    world_region.id
                )
            )
            
            if campaign_region_id is None:
                raise ValueError(
                    "As regiões devem ser snapshotadas "
                    "antes dos locais."
                )
                
            world_locations = (
                self.location_repository
                .get_all_by_region(
                    world_region.id
                )
            )
            
            for world_location in world_locations:
                if (
                    world_location.id
                    in location_id_map
                ):
                    continue
                
                pending_locations.append(
                    (
                        world_location,
                        campaign_region_id,
                    )
                )
                
        created_locations = []
        
        while pending_locations:
            remaining_locations = []
            progress = False
            
            for (
                world_location,
                campaign_region_id
            ) in pending_locations:
                
                parent_id = (
                    world_location.parent_location_id
                )
                
                if parent_id is None:
                    campaign_parent_id = None
                    
                else:
                    campaign_parent_id = (
                        location_id_map.get(
                            parent_id
                        )
                    )
                    
                    if campaign_parent_id is None:
                        remaining_locations.append(
                            (
                                world_location,
                                campaign_region_id
                            )
                        )
                        
                        continue
                    
                campaign_location = (
                    CampaignLocation(
                        campaign_id=campaign.id,
                        region_id=campaign_region_id,
                        parent_location_id=(
                            campaign_parent_id
                        ),
                        source_location_id=(
                            world_location.id
                        ),
                        name=world_location.name,
                        location_type=(
                            world_location.location_type
                        ),
                        description=(
                            world_location.description
                        ),
                        notes=world_location.notes
                    )
                )
                
                self.campaign_location_repository.add(
                    campaign_location
                )
                
                location_id_map[
                    world_location.id
                ] = campaign_location.id
                
                created_locations.append(
                    campaign_location
                )
                
                progress = True
                
            if not progress:
                raise ValueError(
                    "Não foi possível reconstruir "
                    "a hierarquia de locais durante "
                    "o snapshot."
                )
            
            pending_locations = (
                remaining_locations
            )
        
        return created_locations

    def create_initial_snapshot(
        self,
        campaign
    ):
        if campaign.id is None:
            raise ValueError(
                "Não é possível inicializar "
                "uma campanha sem ID."
            )
            
        if campaign.world_id is None:
            raise ValueError(
                "A campanha precisa possuir "
                "um mundo antes do snapshot."
            )
            
        if campaign.snapshot_created_at is not None:
            raise ValueError(
                "Esta campanha já possui "
                "um snapshot inicial."
            )
            
        created_regions = (
            self.snapshot_regions(
                campaign
            )
        )
        
        created_locations = (
            self.snapshot_locations(
                campaign
            )
        )
        
        created_factions = (
            self.snapshot_factions(
                campaign
            )
        )
        
        self.campaign_repository.mark_snapshot_created(
            campaign
        )
        
        return {
            "regions": created_regions,
            "locations": created_locations,
            "factions": created_factions,
        }