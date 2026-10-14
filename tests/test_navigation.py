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


if __name__ == "__main__":
    unittest.main()

