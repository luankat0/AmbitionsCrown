import pygame

from src.core.database import Database
from src.core.navigation import Navigator

from src.domain.campaign.models.campaign import Campaign

from src.core.bootstrap import build_dependencies


from src.domain.campaign.services.campaign_snapshot_service import (
    CampaignSnapshotService,
)


from src.screens.campaign.npcs.list import NPCScreen
from src.screens.campaign.list import CampaignScreen
from src.screens.campaign.regions.detail import RegionScreen
from src.screens.campaign.locations.detail import LocationScreen
from src.screens.campaign.factions.list import FactionScreen

from src.screens.world.library import (
    WorldLibraryScreen,
)
from src.screens.world.overview import (
    WorldManagerScreen,
)
from src.screens.world.regions.detail import (
    WorldRegionScreen
)
from src.screens.world.locations.detail import (
    WorldLocationScreen,
)

from src.screens.world.factions.list import (
    WorldFactionsScreen,
)
from src.screens.world.factions.detail import (
    WorldFactionScreen,
)

class App:
    def __init__(self):
        pygame.init()
        
        self.database = Database()
        self.database.create_tables()
        
        dependencies = build_dependencies(self.database)

        self.npc_repository = dependencies.npc_repository

        self.world_repository = dependencies.world_repository
        self.region_repository = dependencies.region_repository
        self.location_repository = dependencies.location_repository
        self.faction_repository = dependencies.faction_repository

        self.campaign_repository = dependencies.campaign_repository
        self.campaign_region_repository = dependencies.campaign_region_repository
        self.campaign_location_repository = dependencies.campaign_location_repository
        self.campaign_faction_repository = dependencies.campaign_faction_repository

        self.campaign_snapshot_service = (
            dependencies.campaign_snapshot_service
        )
                
        self.campaign_snapshot_service = CampaignSnapshotService(
            self.campaign_repository,
            self.faction_repository,
            self.campaign_faction_repository,
            self.region_repository,
            self.campaign_region_repository,
            self.location_repository,
            self.campaign_location_repository
        )
        
        self.current_campaign: Campaign | None = None

        self.width = 1280
        self.height = 720

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Ambitions Crown")

        self.clock = pygame.time.Clock()
        self.running = True

        self.navigator = Navigator(self)
        
        self.current_screen = CampaignScreen(
            self
        )

    def change_screen(
        self, 
        screen_name
    ):
        screens = {
            "campaigns":
                self.open_campaigns,
            
            "world_library":
                self.open_world_library,
                
            "dashboard":
                self.open_dashboard,
            
            "world":
                self.open_world,
                
            "factions":
                self.open_factions,
            
            "npcs":
                self.open_npcs,
        }
        
        action = screens.get(
            screen_name
        )
        
        if action is None:
            raise ValueError(
                f"Tela desconhecida: {screen_name}"
            )
        
        action()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def render(self):
        self.current_screen.render(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(60)

        self.database.close()
        
        pygame.quit()
        
    def select_campaign(
        self,
        campaign: Campaign
    ):
        self.current_campaign = campaign
        
    def close_campaign(self):
        self.current_campaign = None
        
    def return_to_campaigns(self):
        self.close_campaign()
        self.open_campaigns()
        
    def open_campaigns(self):
        self.navigator.open_campaigns()
        
    def open_dashboard(self):
        self.navigator.open_dashboard()
    
    def open_world(self):
        self.navigator.open_world()
        
    def open_region(self, region):
        self.navigator.open_region(region)

    def open_location(self, region, location):
        self.navigator.open_location(
            region,
            location
        )

    def open_factions(self):
        self.navigator.open_factions()

    def open_npcs(self):
        self.navigator.open_npcs()
        
    def open_world_library(self):
        self.close_campaign()
        
        self.current_screen = (
            WorldLibraryScreen(
                self
            )
        )
        
    def open_world_manager(
        self,
        world
    ):
        self.close_campaign()
        
        self.current_screen = (
            WorldManagerScreen(
                self,
                world
            )
        )
    
    def open_world_region(
        self,
        world,
        region
    ):
        self.close_campaign()
        
        self.current_screen = (
            WorldRegionScreen(
                self,
                world,
                region
            )
        )
        
    def open_world_location(
        self,
        world,
        region,
        location
    ):
        self.close_campaign()
        
        self.current_screen = (
            WorldLocationScreen(
                self,
                world,
                region,
                location
            )
        )

    def open_world_factions(self, world):
        self.close_campaign()
        
        self.current_screen = WorldFactionsScreen(
            self,
            world
        )

    def open_world_faction(
        self,
        world,
        faction
    ):
        self.close_campaign()
        
        self.current_screen = (
            WorldFactionScreen(
                self,
                world,
                faction
            )
        )
