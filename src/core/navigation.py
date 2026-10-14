from src.screens.campaign.list import CampaignScreen
from src.screens.campaign.dashboard import DashboardScreen
from src.screens.campaign.world_overview import WorldScreen


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
