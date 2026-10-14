import pygame

from src.ui.button import Button
from src.ui.scroll import clamp_scroll

from src.ui.region.region_labels import (
    get_region_type_label
)

class RegionListView:
    def __init__(self):
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.new_region_button = Button(
            720,
            290,
            180,
            45,
            "+ Nova Região"
        )
        
        self.card_rects = []
        
        self.list_rect = pygame.Rect(
            300, 355, 600, 325
        )

        self.scroll_offset = 0
        self.scroll_speed = 40
        self.content_height = 0
        
    def handle_event(self, event):
        if self.new_region_button.handle_event(event):
            return "new", None

        if event.type == pygame.MOUSEWHEEL:
            if self.list_rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.scroll_offset = clamp_scroll(
                    self.scroll_offset
                    - event.y * self.scroll_speed,
                    self.content_height,
                    self.list_rect.height
                )

            return None, None

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if not self.list_rect.collidepoint(event.pos):
                return None, None

            for region, rect in self.card_rects:
                if rect.collidepoint(event.pos):
                    return "select", region

        return None, None
    
    def render(self, screen, regions):
        title_surface = self.title_font.render(
            "Regiões",
            True,
            (235, 235, 240)
        )

        screen.blit(
            title_surface,
            (300, 290)
        )

        self.new_region_button.render(screen)

        self.card_rects = []

        self.content_height = max(
            0,
            len(regions) * 90 - 5
        )

        self.scroll_offset = clamp_scroll(
            self.scroll_offset,
            self.content_height,
            self.list_rect.height
        )

        if not regions:
            empty_surface = self.info_font.render(
                "Nenhuma região criada neste mundo.",
                True,
                (150, 150, 160)
            )

            screen.blit(
                empty_surface,
                (300, 365)
            )
            return

        y = (
            self.list_rect.y
            + 10
            - self.scroll_offset
        )

        previous_clip = screen.get_clip()
        screen.set_clip(self.list_rect)

        try:
            for region in regions:
                self._render_region_card(
                    screen,
                    region,
                    y
                )

                y += 90
        finally:
            screen.set_clip(previous_clip)
        
    def _render_region_card(
        self,
        screen,
        region,
        y
    ):
        card_rect = pygame.Rect(
            300,
            y,
            600,
            75
        )
        
        self.card_rects.append(
            (
                region,
                card_rect
            )
        )
        
        pygame.draw.rect(
            screen,
            (45, 45, 55),
            card_rect,
            border_radius=8
        )
        
        name_surface = (
            self.info_font.render(
                region.name,
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            name_surface,
            (
                card_rect.x + 20,
                card_rect.y + 12
            )
        )
        
        type_text = (
            get_region_type_label(
                region.region_type
            )
        )
        
        type_surface = (
            self.info_font.render(
                type_text,
                True,
                (155, 155, 165)
            )
        )
        
        screen.blit(
            type_surface,
            (
                card_rect.x + 20,
                card_rect.y + 42
            )
        )
        
