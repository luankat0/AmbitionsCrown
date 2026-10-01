import pygame

from src.ui.button import Button

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
        
    def handle_event(
        self,
        event
    ):
        if self.new_region_button.handle_event(
            event
        ):
            return "new", None
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for region, rect in self.card_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    return "select", region
                
        return None, None
    
    def render(
        self,
        screen,
        regions
    ):
        title_surface = (
            self.title_font.render(
                "Regiões",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            title_surface,
            (300, 290)
        )
        
        self.new_region_button.render(
            screen
        )
        
        self.card_rects = []
        
        if not regions:
            empty_surface = (
                self.info_font.render(
                    "Nenhuma região criada neste mundo.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (300, 365)
            )
            
            return
        
        y = 365
        
        for region in regions:
            self._render_region_card(
                screen,
                region,
                y
            )
            
            y += 90
            
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
        
