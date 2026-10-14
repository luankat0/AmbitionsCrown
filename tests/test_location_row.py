import unittest
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import pygame

from src.domain.world.models.location import LocationType

from src.ui.location_row import draw_location_row

from src.ui.location.location_children_view import (
    LocationChildrenView,
)

from src.ui.location.location_tree_view import (
    LocationTreeView,
)


class LocationRowTests(unittest.TestCase):

    def test_row_preserves_colors_and_positions(self):
        screen = Mock()
        font = Mock()

        draw_location_row(
            screen=screen,
            font=font,
            name="Torre do Mago",
            location_type_label="Torre",
            x=300,
            y=575,
            type_offset=280
        )

        self.assertEqual(
            font.render.call_args_list,
            [
                call(
                    "Torre do Mago",
                    True,
                    (220, 220, 230)
                ),
                call(
                    "Torre",
                    True,
                    (145, 145, 160)
                )
            ]
        )

        self.assertEqual(
            screen.blit.call_args_list,
            [
                call(font.render.return_value, (300, 575)),
                call(font.render.return_value, (580, 575))
            ]
        )

    def test_children_preserve_hitboxes(self):
        view = LocationChildrenView.__new__(
            LocationChildrenView
        )

        view.info_font = Mock()

        child = SimpleNamespace(
            name="Torre",
            location_type=LocationType.TOWER
        )

        screen = Mock()

        with patch(
            "src.ui.location.location_children_view.draw_location_row"
        ) as draw_row:
            view.render(
                screen,
                [child],
                start_x=300,
                start_y=575
            )

            draw_row.assert_called_once_with(
                screen=screen,
                font=view.info_font,
                name="Torre",
                location_type_label="Torre",
                x=300,
                y=575,
                type_offset=280
            )

        self.assertEqual(
            view.child_rects,
            [
                (
                    child,
                    pygame.Rect(300, 571, 580, 34)
                )
            ]
        )

    def test_tree_preserves_hierarchy_and_hitboxes(self):
        view = LocationTreeView.__new__(
            LocationTreeView
        )

        view.info_font = Mock()
        view.indent_width = 28
        view.row_height = 38

        city = SimpleNamespace(
            id=1,
            parent_location_id=None,
            name="Cidade",
            location_type=LocationType.CITY
        )

        castle = SimpleNamespace(
            id=2,
            parent_location_id=1,
            name="Castelo",
            location_type=LocationType.CASTLE
        )

        screen = Mock()

        with patch(
            "src.ui.location.location_tree_view.draw_location_row"
        ) as draw_row:
            view.render(
                screen,
                [city, castle],
                start_x=300,
                start_y=575
            )

            self.assertEqual(
                draw_row.call_args_list,
                [
                    call(
                        screen=screen,
                        font=view.info_font,
                        name="• Cidade",
                        location_type_label="Cidade",
                        x=300,
                        y=575,
                        type_offset=260
                    ),
                    call(
                        screen=screen,
                        font=view.info_font,
                        name="Castelo",
                        location_type_label="Castelo",
                        x=328,
                        y=613,
                        type_offset=260
                    )
                ]
            )

        self.assertEqual(
            view.location_rects,
            [
                (
                    city,
                    pygame.Rect(300, 571, 500, 38)
                ),
                (
                    castle,
                    pygame.Rect(328, 609, 472, 38)
                )
            ]
        )


if __name__ == "__main__":
    unittest.main()

