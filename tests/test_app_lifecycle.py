import unittest
from typing import cast
from unittest.mock import Mock, patch

import pygame

from src.core.app import App
from src.core.database import Database


class AppLifecycleTests(unittest.TestCase):

    def setUp(self):
        # Evita inicializar Pygame e SQLite.
        self.app = App.__new__(App)

        self.database_mock = Mock()
        self.clock_mock = Mock()

        self.app.database = cast(
            Database,
            self.database_mock
        )

        self.app.clock = cast(
            pygame.time.Clock,
            self.clock_mock
        )

        self.app.running = True

    def test_normal_shutdown_closes_resources(self):
        def stop_application():
            self.app.running = False

        with (
            patch.object(
                App,
                "handle_events",
                side_effect=stop_application
            ),
            patch.object(App, "update") as update,
            patch.object(App, "render") as render,
            patch("src.core.app.pygame.quit") as quit_pygame,
        ):
            self.app.run()

            update.assert_called_once_with()
            render.assert_called_once_with()

            self.clock_mock.tick.assert_called_once_with(60)

            self.database_mock.close.assert_called_once_with()
            quit_pygame.assert_called_once_with()

    def test_render_failure_still_closes_resources(self):
        with (
            patch.object(App, "handle_events"),
            patch.object(App, "update"),
            patch.object(
                App,
                "render",
                side_effect=RuntimeError(
                    "Falha simulada no render"
                )
            ),
            patch("src.core.app.pygame.quit") as quit_pygame,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha simulada no render"
            ):
                self.app.run()

            self.database_mock.close.assert_called_once_with()
            quit_pygame.assert_called_once_with()

            # A execução falhou antes de atualizar o FPS.
            self.clock_mock.tick.assert_not_called()

    def test_pygame_quits_even_if_database_close_fails(self):
        def stop_application():
            self.app.running = False

        self.database_mock.close.side_effect = RuntimeError(
            "Falha ao fechar SQLite"
        )

        with (
            patch.object(
                App,
                "handle_events",
                side_effect=stop_application
            ),
            patch.object(App, "update"),
            patch.object(App, "render"),
            patch("src.core.app.pygame.quit") as quit_pygame,
        ):
            with self.assertRaisesRegex(
                RuntimeError,
                "Falha ao fechar SQLite"
            ):
                self.app.run()

            self.database_mock.close.assert_called_once_with()
            quit_pygame.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

