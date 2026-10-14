import unittest
from unittest.mock import Mock, call, patch, sentinel

import pygame

from src.ui.region.region_details_view import (
    RegionDetailsView,
)


class RegionDetailsScrollTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.font_initialized = pygame.font.get_init()

        if not cls.font_initialized:
            pygame.font.init()

    @classmethod
    def tearDownClass(cls):
        if not cls.font_initialized:
            pygame.font.quit()

    def setUp(self):
        self.view = RegionDetailsView()

    def test_mouse_wheel_scroll_and_limits(self):
        self.view.content_height = 380

        with patch(
            "src.ui.region.region_details_view.pygame.mouse.get_pos",
            return_value=(400, 600)
        ):
            self.view.handle_event(
                pygame.event.Event(
                    pygame.MOUSEWHEEL,
                    {"y": -1}
                )
            )

            self.assertEqual(
                self.view.scroll_offset,
                38
            )

            self.view.handle_event(
                pygame.event.Event(
                    pygame.MOUSEWHEEL,
                    {"y": -100}
                )
            )

            self.assertEqual(
                self.view.scroll_offset,
                250
            )

            self.view.handle_event(
                pygame.event.Event(
                    pygame.MOUSEWHEEL,
                    {"y": 100}
                )
            )

            self.assertEqual(
                self.view.scroll_offset,
                0
            )

    def test_scroll_only_works_inside_list(self):
        self.view.content_height = 380

        with patch(
            "src.ui.region.region_details_view.pygame.mouse.get_pos",
            return_value=(400, 400)
        ):
            self.view.handle_event(
                pygame.event.Event(
                    pygame.MOUSEWHEEL,
                    {"y": -1}
                )
            )

        self.assertEqual(
            self.view.scroll_offset,
            0
        )

    def test_clicks_outside_list_are_ignored(self):
        outside = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": (320, 560)}
        )

        inside = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"button": 1, "pos": (320, 600)}
        )

        with patch.object(
            self.view.location_tree_view,
            "handle_event",
            return_value=sentinel.location
        ) as tree_handler:

            self.assertEqual(
                self.view.handle_event(outside),
                (None, None)
            )

            tree_handler.assert_not_called()

            self.assertEqual(
                self.view.handle_event(inside),
                ("select_location", sentinel.location)
            )

            tree_handler.assert_called_once_with(inside)

    def test_render_clips_and_shifts_location_tree(self):
        screen = Mock()
        previous_clip = pygame.Rect(0, 0, 1280, 720)
        screen.get_clip.return_value = previous_clip

        locations = [object()] * 6
        self.view.scroll_offset = 200

        with (
            patch.object(self.view.new_location_button, "render"),
            patch.object(
                self.view.location_tree_view,
                "render"
            ) as tree_render,
        ):
            self.view._render_locations_section(
                screen,
                locations
            )

        # Seis linhas de 38 px: 228 px de conteúdo.
        # Área visível de 130 px: limite de 98 px.
        self.assertEqual(self.view.scroll_offset, 98)

        tree_render.assert_called_once_with(
            screen,
            locations,
            start_x=300,
            start_y=477
        )

        self.assertEqual(
            screen.set_clip.call_args_list,
            [
                call(self.view.locations_viewport),
                call(previous_clip)
            ]
        )


if __name__ == "__main__":
    unittest.main()

