import pygame

from src.ui.location.location_labels import (
    get_location_type_label
)


class LocationChildrenView:
    def __init__(self):
        self.info_font = pygame.font.Font(
            None,
            24
        )

    def render(
        self,
        screen,
        children,
        start_x,
        start_y
    ):
        if not children:
            empty_surface = (
                self.info_font.render(
                    "Nenhum sublocal criado.",
                    True,
                    (150, 150, 160)
                )
            )

            screen.blit(
                empty_surface,
                (
                    start_x,
                    start_y
                )
            )

            return

        y = start_y

        for location in children:
            self._render_child(
                screen,
                location,
                start_x,
                y
            )

            y += 38

    def _render_child(
        self,
        screen,
        location,
        x,
        y
    ):
        name_surface = (
            self.info_font.render(
                location.name,
                True,
                (220, 220, 230)
            )
        )

        screen.blit(
            name_surface,
            (
                x,
                y
            )
        )

        type_text = (
            get_location_type_label(
                location.location_type
            )
        )

        type_surface = (
            self.info_font.render(
                type_text,
                True,
                (145, 145, 160)
            )
        )

        screen.blit(
            type_surface,
            (
                x + 280,
                y
            )
        )