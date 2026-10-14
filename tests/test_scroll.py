import unittest

import pygame

from src.ui.scroll import clamp_scroll

from src.screens.world.regions.detail import (
    WorldRegionScreen,
)

from src.screens.world.locations.detail import (
    WorldLocationScreen,
)


class ScrollTests(unittest.TestCase):

    def test_empty_content_has_no_scroll(self):
        self.assertEqual(
            clamp_scroll(100, 0, 320),
            0
        )

    def test_content_smaller_than_viewport(self):
        self.assertEqual(
            clamp_scroll(100, 200, 320),
            0
        )

    def test_valid_scroll_is_preserved(self):
        self.assertEqual(
            clamp_scroll(40, 500, 320),
            40
        )

    def test_scroll_cannot_be_negative(self):
        self.assertEqual(
            clamp_scroll(-50, 500, 320),
            0
        )

    def test_region_scroll_uses_shared_bounds(self):
        screen = WorldRegionScreen.__new__(
            WorldRegionScreen
        )

        screen.locations = [object()] * 4
        screen.list_rect = pygame.Rect(
            0, 0, 850, 320
        )
        screen.scroll_offset = 999

        screen._clamp_scroll()

        # 4 cards * 90 - 5 = 355
        # 355 - 320 = 35
        self.assertEqual(
            screen.scroll_offset,
            35
        )

    def test_location_scroll_uses_shared_bounds(self):
        screen = WorldLocationScreen.__new__(
            WorldLocationScreen
        )

        screen.children = [object()] * 5
        screen.list_rect = pygame.Rect(
            0, 0, 850, 320
        )
        screen.scroll_offset = 999

        screen._clamp_scroll()

        # 5 cards * 90 - 5 = 445
        # 445 - 320 = 125
        self.assertEqual(
            screen.scroll_offset,
            125
        )


if __name__ == "__main__":
    unittest.main()

