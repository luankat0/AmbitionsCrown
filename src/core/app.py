import pygame

from src.core.database import Database

from src.models.campaign import Campaign

from src.repositories.npc_repository import NPCRepository
from src.repositories.campaign_repository import CampaignRepository
from src.repositories.world_repository import WorldRepository
from src.repositories.region_repository import RegionRepository
from src.repositories.location_repository import LocationRepository
from src.repositories.faction_repository import FactionRepository

from src.screens.dashboard import DashboardScreen
from src.screens.npcs import NPCScreen
from src.screens.campaigns import CampaignScreen
from src.screens.worlds import WorldScreen
from src.screens.regions import RegionScreen
from src.screens.locations import LocationScreen

class App:
    def __init__(self):
        pygame.init()
        
        self.database = Database()
        self.database.create_tables()
        
        self.npc_repository = NPCRepository(
            self.database
        )
        
        self.campaign_repository = CampaignRepository(
            self.database
        )
        
        self.world_repository = WorldRepository(
            self.database
        )
        
        self.region_repository = RegionRepository(
            self.database
        )
        
        self.location_repository = LocationRepository(
            self.database
        )
        
        self.faction_repository = FactionRepository(
            self.database
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
                
            "dashboard":
                self.open_dashboard,
            
            "world":
                self.open_world,
            
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
        
    def open_region(
        self,
        region
    ):
        if self.current_campaign is None:
            return
        
        self.current_screen = (
            RegionScreen(
                self,
                region
            )
        )

    def open_location(
        self,
        region,
        location
    ):
        if self.current_campaign is None:
            return
        
        self.current_screen = (
            LocationScreen(
                self,
                region,
                location
            )
        )

    def open_campaigns(self):
        self.current_screen = (
            CampaignScreen(self)
        )
        
    def open_dashboard(self):
        if self.current_campaign is None:
            return
        
        self.current_screen = (
            DashboardScreen(self)
        )
    
    def open_world(self):
        if self.current_campaign is None:
            return
        
        self.current_screen = (
            WorldScreen(self)
        )
    
    def open_npcs(self):
        if self.current_campaign is None:
            return
        
        self.current_screen = (
            NPCScreen(self)
        )
