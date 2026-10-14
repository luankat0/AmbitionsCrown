import unittest

from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import pygame

from src.ui.location_card import draw_location_card

from src.screens.world.regions.detail import (
    WorldRegionScreen,
)
from src.screens.world.locations.detail import (
    WorldLocationScreen,
)


class LocationCardTests(unittest.TestCase):

    def test_card_preserves_visual_style(self):
        surface = Mock()
        rect = pygame.Rect(80, 340, 760, 75)

        name_font = Mock()
        info_font = Mock()

        with patch(
            "src.ui.location_card.pygame.draw.rect"
        ) as draw_rect:
            draw_location_card(
                surface,
                rect,
                "Torre do Mago",
                "",
                name_font,
                info_font
            )

        draw_rect.assert_called_once_with(
            surface,
            (45, 45, 55),
            rect,
            border_radius=8
        )

        name_font.render.assert_called_once_with(
            "Torre do Mago",
            True,
            (235, 235, 240)
        )

        info_font.render.assert_called_once_with(
            "Sem descrição.",
            True,
            (155, 155, 165)
        )

        self.assertEqual(
            surface.blit.call_args_list,
            [
                call(
                    name_font.render.return_value,
                    (100, 350)
                ),
                call(
                    info_font.render.return_value,
                    (100, 385)
                ),
            ]
        )

    def test_both_screens_preserve_card_hitboxes(self):
        cases = (
            (
                WorldRegionScreen,
                "locations",
                "location_card_rects",
                "render_locations",
                "src.screens.world.regions.detail.draw_location_card"
            ),
            (
                WorldLocationScreen,
                "children",
                "child_card_rects",
                "render_children",
                "src.screens.world.locations.detail.draw_location_card"
            ),
        )

        for (
            screen_class,
            items_attribute,
            rects_attribute,
            render_method,
            patch_path
        ) in cases:
            with self.subTest(screen=screen_class.__name__):
                instance = screen_class.__new__(
                    screen_class
                )

                location = SimpleNamespace(
                    name="Cidade",
                    description="Capital do reino"
                )

                setattr(
                    instance,
                    items_attribute,
                    [location]
                )

                instance.list_rect = pygame.Rect(
                    80, 330, 850, 320
                )
                instance.scroll_offset = 0

                instance.name_font = Mock()
                instance.info_font = Mock()

                surface = Mock()
                previous_clip = pygame.Rect(
                    0, 0, 1280, 720
                )
                surface.get_clip.return_value = previous_clip

                with patch(patch_path) as draw_card:
                    getattr(
                        instance,
                        render_method
                    )(surface)

                expected_rect = pygame.Rect(
                    80, 340, 760, 75
                )

                draw_card.assert_called_once_with(
                    surface,
                    expected_rect,
                    "Cidade",
                    "Capital do reino",
                    instance.name_font,
                    instance.info_font
                )

                self.assertEqual(
                    getattr(instance, rects_attribute),
                    [(location, expected_rect)]
                )

                self.assertEqual(
                    surface.set_clip.call_args_list,
                    [
                        call(instance.list_rect),
                        call(previous_clip),
                    ]
                )


if __name__ == "__main__":
    unittest.main()