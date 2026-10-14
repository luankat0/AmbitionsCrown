import unittest
from unittest.mock import patch

from src.core.app import App
from src.core.navigation import Navigator


class AppStartupTests(unittest.TestCase):

    def test_app_initializes_first_screen_through_navigator(self):
        with (
            patch("src.core.app.pygame.init"),
            patch("src.core.app.pygame.display.set_mode"),
            patch("src.core.app.pygame.display.set_caption"),
            patch("src.core.app.pygame.time.Clock"),
            patch("src.core.app.Database") as database_class,
            patch("src.core.app.build_dependencies"),
            patch("src.core.navigation.CampaignScreen") as screen_class,
        ):
            app = App()

            # Navigator deve ter sido inicializado.
            self.assertIsInstance(
                app.navigator,
                Navigator
            )

            # CampaignScreen deve receber a instância de App.
            screen_class.assert_called_once_with(app)

            # A tela inicial deve vir do Navigator.
            self.assertIs(
                app.current_screen,
                screen_class.return_value
            )

            # O Workspace começa sem Campaign ativa.
            self.assertIsNone(
                app.current_campaign
            )

            # O banco foi preparado.
            database_class.return_value.create_tables.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()