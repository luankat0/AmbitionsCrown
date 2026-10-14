import pygame

from src.ui.location_row import draw_location_row

from src.ui.location.location_labels import (
    get_location_type_label
)


class LocationChildrenView:
    def __init__(self):
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.child_rects = []
        
    def handle_event(
        self,
        event
    ):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for location, rect in self.child_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    return location
        
        return None

    def render(
        self,
        screen,
        children,
        start_x,
        start_y
    ):
        self.child_rects = []        

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
        row_rect = pygame.Rect(
            x,
            y - 4,
            580,
            34
        )
        
        self.child_rects.append(
            (
                location,
                row_rect
            )
        )
        
        draw_location_row(
            screen=screen,
            font=self.info_font,
            name=location.name,
            location_type_label=get_location_type_label(
                location.location_type
            ),
            x=x,
            y=y,
            type_offset=280
        )
