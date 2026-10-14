import pygame

from src.core.database import Database
from src.core.navigation import Navigator
from src.core.workspace import Workspace
from src.core.bootstrap import build_dependencies

from src.domain.campaign.models.campaign import Campaign

from src.domain.campaign.services.campaign_snapshot_service import (
    CampaignSnapshotService,
)

from src.screens.base_screen import BaseScreen


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
        
        self.workspace = Workspace()

        self.width = 1280
        self.height = 720

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Ambitions Crown")

        self.clock = pygame.time.Clock()
        self.running = True
        
        self.current_screen: BaseScreen

        self.navigator = Navigator(self)
        
        self.navigator.open_campaigns()

    @property
    def current_campaign(self) -> Campaign | None:
        return self.workspace.current_campaign

    def change_screen(self, screen_name: str):
        self.navigator.change_screen(screen_name)
        
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
        
    def select_campaign(self, campaign: Campaign):
        self.workspace.select_campaign(campaign)
        
    def close_campaign(self):
        self.workspace.close_campaign()
        
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
        self.navigator.open_world_library()
        
    def open_world_manager(self, world):
        self.navigator.open_world_manager(world)
    
    def open_world_region(self, world, region):
        self.navigator.open_world_region(world, region)
        
    def open_world_location(self, world, region, location):
        self.navigator.open_world_location(world, region, location)

    def open_world_factions(self, world):
        self.navigator.open_world_factions(world)

    def open_world_faction(self, world, faction):
        self.navigator.open_world_faction(world, faction)

