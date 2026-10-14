import unittest
from types import SimpleNamespace
from unittest.mock import patch, sentinel

from src.core.navigation import Navigator


class NavigationTests(unittest.TestCase):

    def setUp(self):
        self.app = SimpleNamespace(
            current_campaign=None,
            current_screen=sentinel.previous_screen
        )

        self.navigator = Navigator(self.app)

    def test_open_campaigns(self):
        with patch(
            "src.core.navigation.CampaignScreen"
        ) as screen_class:

            self.navigator.open_campaigns()

            screen_class.assert_called_once_with(
                self.app
            )

            self.assertIs(
                self.app.current_screen,
                screen_class.return_value
            )

    def test_dashboard_requires_active_campaign(self):
        with patch(
            "src.core.navigation.DashboardScreen"
        ) as screen_class:

            self.navigator.open_dashboard()

            screen_class.assert_not_called()

            self.assertIs(
                self.app.current_screen,
                sentinel.previous_screen
            )

    def test_world_requires_active_campaign(self):
        with patch(
            "src.core.navigation.WorldScreen"
        ) as screen_class:

            self.navigator.open_world()

            screen_class.assert_not_called()

            self.assertIs(
                self.app.current_screen,
                sentinel.previous_screen
            )

    def test_dashboard_and_world_with_active_campaign(self):
        self.app.current_campaign = SimpleNamespace(
            id=1,
            world_id=2
        )

        with patch(
            "src.core.navigation.DashboardScreen"
        ) as dashboard_class:

            self.navigator.open_dashboard()

            dashboard_class.assert_called_once_with(
                self.app
            )

            self.assertIs(
                self.app.current_screen,
                dashboard_class.return_value
            )

        with patch(
            "src.core.navigation.WorldScreen"
        ) as world_class:

            self.navigator.open_world()

            world_class.assert_called_once_with(
                self.app
            )

            self.assertIs(
                self.app.current_screen,
                world_class.return_value
            )

    def test_region_and_location_require_campaign(self):
        with (
            patch("src.core.navigation.RegionScreen") as region_screen,
            patch("src.core.navigation.LocationScreen") as location_screen,
        ):
            self.navigator.open_region(sentinel.region)

            self.navigator.open_location(
                sentinel.region,
                sentinel.location
            )

            region_screen.assert_not_called()
            location_screen.assert_not_called()

            self.assertIs(
                self.app.current_screen,
                sentinel.previous_screen
            )


    def test_open_region_and_location_with_campaign(self):
        self.app.current_campaign = SimpleNamespace(
            id=1,
            world_id=2
        )

        with patch(
            "src.core.navigation.RegionScreen"
        ) as region_screen:
            self.navigator.open_region(sentinel.region)

            region_screen.assert_called_once_with(
                self.app,
                sentinel.region
            )

            self.assertIs(
                self.app.current_screen,
                region_screen.return_value
            )

        with patch(
            "src.core.navigation.LocationScreen"
        ) as location_screen:
            self.navigator.open_location(
                sentinel.region,
                sentinel.location
            )

            location_screen.assert_called_once_with(
                self.app,
                sentinel.region,
                sentinel.location
            )

            self.assertIs(
                self.app.current_screen,
                location_screen.return_value
            )


    def test_factions_and_npcs_require_campaign(self):
        with (
            patch("src.core.navigation.FactionScreen") as faction_screen,
            patch("src.core.navigation.NPCScreen") as npc_screen,
        ):
            self.navigator.open_factions()
            self.navigator.open_npcs()

            faction_screen.assert_not_called()
            npc_screen.assert_not_called()

            self.assertIs(
                self.app.current_screen,
                sentinel.previous_screen
            )


    def test_open_factions_and_npcs_with_campaign(self):
        self.app.current_campaign = SimpleNamespace(
            id=1,
            world_id=2
        )

        with patch(
            "src.core.navigation.FactionScreen"
        ) as faction_screen:
            self.navigator.open_factions()

            faction_screen.assert_called_once_with(
                self.app
            )

            self.assertIs(
                self.app.current_screen,
                faction_screen.return_value
            )

        with patch(
            "src.core.navigation.NPCScreen"
        ) as npc_screen:
            self.navigator.open_npcs()

            npc_screen.assert_called_once_with(
                self.app
            )

            self.assertIs(
                self.app.current_screen,
                npc_screen.return_value
            )

if __name__ == "__main__":
    unittest.main()

