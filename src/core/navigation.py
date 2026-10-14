from src.screens.campaign.list import CampaignScreen
from src.screens.campaign.dashboard import DashboardScreen
from src.screens.campaign.world_overview import WorldScreen
from src.screens.campaign.regions.detail import RegionScreen
from src.screens.campaign.locations.detail import LocationScreen
from src.screens.campaign.factions.list import FactionScreen
from src.screens.campaign.npcs.list import NPCScreen


class Navigator:
    def __init__(self, app):
        self.app = app

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
