from src.screens.campaign.list import CampaignScreen
from src.screens.campaign.dashboard import DashboardScreen
from src.screens.campaign.world_overview import WorldScreen
from src.screens.campaign.regions.detail import RegionScreen
from src.screens.campaign.locations.detail import LocationScreen
from src.screens.campaign.factions.list import FactionScreen
from src.screens.campaign.npcs.list import NPCScreen

from src.screens.world.library import WorldLibraryScreen
from src.screens.world.overview import WorldManagerScreen
from src.screens.world.regions.detail import WorldRegionScreen
from src.screens.world.locations.detail import WorldLocationScreen
from src.screens.world.factions.list import WorldFactionsScreen
from src.screens.world.factions.detail import WorldFactionScreen


class Navigator:
    def __init__(self, app):
        self.app = app
        
    def change_screen(self, screen_name: str) -> None:
        screens = {
            "campaigns": self.open_campaigns,
            "world_library": self.open_world_library,
            "dashboard": self.open_dashboard,
            "world": self.open_world,
            "factions": self.open_factions,
            "npcs": self.open_npcs,
        }

        action = screens.get(screen_name)

        if action is None:
            raise ValueError(
                f"Tela desconhecida: {screen_name}"
            )

        action()

    def open_campaigns(self):
        self.app.current_screen = CampaignScreen(
            self.app
        )

    def open_dashboard(self):
        if self.app.current_campaign is None:
            return

        self.app.current_screen = DashboardScreen(
            self.app
        )

    def open_world(self):
        if self.app.current_campaign is None:
            return

        self.app.current_screen = WorldScreen(
            self.app
        )
    
    def open_region(self, region):
        if self.app.current_campaign is None:
            return

        self.app.current_screen = RegionScreen(
            self.app,
            region
        )

    def open_location(self, region, location):
        if self.app.current_campaign is None:
            return

        self.app.current_screen = LocationScreen(
            self.app,
            region,
            location
        )

    def open_factions(self):
        if self.app.current_campaign is None:
            return

        self.app.current_screen = FactionScreen(
            self.app
        )

    def open_npcs(self):
        if self.app.current_campaign is None:
            return

        self.app.current_screen = NPCScreen(
            self.app
        )

    def open_world_library(self):
        self.app.close_campaign()

        self.app.current_screen = WorldLibraryScreen(
            self.app
        )

    def open_world_manager(self, world):
        self.app.close_campaign()

        self.app.current_screen = WorldManagerScreen(
            self.app,
            world
        )

    def open_world_region(self, world, region):
        self.app.close_campaign()

        self.app.current_screen = WorldRegionScreen(
            self.app,
            world,
            region
        )

    def open_world_location(self, world, region, location):
        self.app.close_campaign()

        self.app.current_screen = WorldLocationScreen(
            self.app,
            world,
            region,
            location
        )

    def open_world_factions(self, world):
        self.app.close_campaign()

        self.app.current_screen = WorldFactionsScreen(
            self.app,
            world
        )

    def open_world_faction(self, world, faction):
        self.app.close_campaign()

        self.app.current_screen = WorldFactionScreen(
            self.app,
            world,
            faction
        )

