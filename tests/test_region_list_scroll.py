import unittest
from types import SimpleNamespace
from unittest.mock import patch

import pygame

from src.domain.world.models.region import RegionType
from src.ui.region.region_list_view import RegionListView


class RegionListScrollTests(unittest.TestCase):

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
        self.view = RegionListView()
        self.screen = pygame.Surface((1280, 720))

        self.regions = [
            SimpleNamespace(
                name=f"Região {i}",
                region_type=RegionType.OTHER
            )
            for i in range(8)
        ]

        self.view.render(
            self.screen,
            self.regions
        )

    def test_scroll_respects_limits(self):
        wheel = pygame.event.Event(
            pygame.MOUSEWHEEL,
            {"y": -1}
        )

        with patch(
            "src.ui.region.region_list_view.pygame.mouse.get_pos",
            return_value=(400, 450)
        ):
            self.view.handle_event(wheel)

            self.assertEqual(
                self.view.scroll_offset,
                40
            )

            self.view.handle_event(
                pygame.event.Event(
                    pygame.MOUSEWHEEL,
                    {"y": -100}
                )
            )

            self.assertEqual(
                self.view.scroll_offset,
                390
            )

    def test_scroll_outside_list_is_ignored(self):
        with patch(
            "src.ui.region.region_list_view.pygame.mouse.get_pos",
            return_value=(400, 200)
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

    def test_last_region_is_accessible_after_scroll(self):
        self.view.scroll_offset = 390

        self.view.render(
            self.screen,
            self.regions
        )

        last_region, rect = self.view.card_rects[-1]

        self.assertEqual(
            rect.bottom,
            self.view.list_rect.bottom
        )

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {
                "button": 1,
                "pos": (320, rect.y + 15)
            }
        )

        self.assertEqual(
            self.view.handle_event(event),
            ("select", last_region)
        )

    def test_hidden_card_cannot_be_clicked(self):
        self.view.scroll_offset = 20

        self.view.render(
            self.screen,
            self.regions
        )

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {
                "button": 1,
                "pos": (320, 350)
            }
        )

        self.assertEqual(
            self.view.handle_event(event),
            (None, None)
        )


if __name__ == "__main__":
    unittest.main()

