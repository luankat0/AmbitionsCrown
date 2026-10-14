import unittest
from unittest.mock import Mock, patch, sentinel

from types import SimpleNamespace

from src.core.app import App
from src.core.navigation import Navigator


class NavigationTests(unittest.TestCase):

    def setUp(self):
        self.app = SimpleNamespace(
            current_campaign=None,
            current_screen=sentinel.previous_screen
        )

        self.navigator = Navigator(self.app)

    def assert_world_route_closes_campaign(
        self,
        method_name,
        screen_class_name,
        *screen_args
    ):
        self.app.current_campaign = SimpleNamespace(
            id=1,
            world_id=2
        )

        self.app.current_screen = sentinel.previous_screen

        close_campaign = Mock(
            side_effect=lambda: setattr(
                self.app,
                "current_campaign",
                None
            )
        )

        self.app.close_campaign = close_campaign

        def create_screen(*received_args):
            # A Campaign precisa ser encerrada
            # antes da criação da próxima tela.
            self.assertIsNone(
                self.app.current_campaign
            )

            self.assertEqual(
                received_args,
                (self.app, *screen_args)
            )

            return sentinel.destination_screen

        with patch(
            f"src.core.navigation.{screen_class_name}",
            side_effect=create_screen
        ) as screen_class:

            route = getattr(
                self.navigator,
                method_name
            )

            route(*screen_args)

            close_campaign.assert_called_once_with()

            screen_class.assert_called_once_with(
                self.app,
                *screen_args
            )

            self.assertIs(
                self.app.current_screen,
                sentinel.destination_screen
            )

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

    def test_world_library_closes_campaign_before_opening(self):
        self.app.current_campaign = SimpleNamespace(
            id=1,
            world_id=2
        )

        close_campaign = Mock(
            side_effect=lambda: setattr(
                self.app,
                "current_campaign",
                None
            )
        )

        self.app.close_campaign = close_campaign

        def create_screen(app):
            self.assertIsNone(app.current_campaign)
            return sentinel.world_library_screen

        with patch(
            "src.core.navigation.WorldLibraryScreen",
            side_effect=create_screen
        ) as screen_class:

            self.navigator.open_world_library()

            close_campaign.assert_called_once_with()
            screen_class.assert_called_once_with(self.app)

            self.assertIs(
                self.app.current_screen,
                sentinel.world_library_screen
            )

    def test_world_manager_closes_campaign_before_opening(self):
        self.app.current_campaign = SimpleNamespace(
            id=1,
            world_id=2
        )

        close_campaign = Mock(
            side_effect=lambda: setattr(
                self.app,
                "current_campaign",
                None
            )
        )

        self.app.close_campaign = close_campaign

        def create_screen(app, world):
            self.assertIsNone(app.current_campaign)

            self.assertIs(
                world,
                sentinel.canonical_world
            )

            return sentinel.world_manager_screen

        with patch(
            "src.core.navigation.WorldManagerScreen",
            side_effect=create_screen
        ) as screen_class:

            self.navigator.open_world_manager(
                sentinel.canonical_world
            )

            close_campaign.assert_called_once_with()

            screen_class.assert_called_once_with(
                self.app,
                sentinel.canonical_world
            )

            self.assertIs(
                self.app.current_screen,
                sentinel.world_manager_screen
            )

    def test_world_region_navigation(self):
        self.assert_world_route_closes_campaign(
            "open_world_region",
            "WorldRegionScreen",
            sentinel.canonical_world,
            sentinel.region
        )

    def test_world_location_navigation(self):
        self.assert_world_route_closes_campaign(
            "open_world_location",
            "WorldLocationScreen",
            sentinel.canonical_world,
            sentinel.region,
            sentinel.location
        )

    def test_world_factions_navigation(self):
        self.assert_world_route_closes_campaign(
            "open_world_factions",
            "WorldFactionsScreen",
            sentinel.canonical_world
        )

    def test_world_faction_navigation(self):
        self.assert_world_route_closes_campaign(
            "open_world_faction",
            "WorldFactionScreen",
            sentinel.canonical_world,
            sentinel.faction
        )
        
    def test_change_screen_dispatches_menu_routes(self):
        routes = {
            "campaigns": "open_campaigns",
            "world_library": "open_world_library",
            "dashboard": "open_dashboard",
            "world": "open_world",
            "factions": "open_factions",
            "npcs": "open_npcs",
        }

        for screen_name, method_name in routes.items():
            with self.subTest(screen=screen_name):
                with patch.object(
                    self.navigator,
                    method_name
                ) as route:

                    self.navigator.change_screen(
                        screen_name
                    )

                    route.assert_called_once_with()


    def test_change_screen_rejects_unknown_route(self):
        with self.assertRaisesRegex(
            ValueError,
            "Tela desconhecida: invalid_screen"
        ):
            self.navigator.change_screen(
                "invalid_screen"
            )

class AppNavigationCompatibilityTests(unittest.TestCase):

    def test_app_change_screen_delegates_to_navigator(self):
        # Não executa App.__init__().
        # Portanto, não abre janela nem conexão SQLite.
        app = App.__new__(App)

        app.navigator = Navigator(app)

        with patch.object(
            app.navigator,
            "change_screen"
        ) as navigate:

            app.change_screen("dashboard")

            navigate.assert_called_once_with(
                "dashboard"
            )

if __name__ == "__main__":
    unittest.main()

