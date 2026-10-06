import pygame

from src.ui.button import Button
from src.ui.faction.faction_labels import (
    get_faction_status_label,
    get_faction_type_label
)


class FactionListView:
    def __init__(self):
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.new_button = Button(
            300,
            160,
            180,
            45,
            "+ Nova Facção"
        )
        
        self.faction_rects = []
        
    def handle_event(
        self,
        event
    ):
        if self.new_button.handle_event(
            event
        ):
            return "new", None
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for faction, rect in (
                self.faction_rects
            ):
                if rect.collidepoint(
                    event.pos
                ):
                    return "select", faction
        
        return None, None
    
    def render(
        self,
        screen,
        factions
    ):
        title_surface = (
            self.title_font.render(
                "Facções",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            title_surface,
            (300, 100)
        )
        
        self.new_button.render(
            screen
        )
        
        self.faction_rects = []
        
        if not factions:
            empty_surface = (
                self.info_font.render(
                    "Nenhuma facção criada ainda.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (300, 240)
            )
            
            return
        
        y = 240
        
        for faction in factions:
            self._render_faction(
                screen,
                faction,
                y
            )
            
            y += 55
            
    def _render_faction(
        self,
        screen,
        faction,
        y
    ):
        row_rect = pygame.Rect(
            300,
            y - 8,
            720,
            45
        )
        
        self.faction_rects.append(
            (
                faction,
                row_rect
            )
        )
        
        name_surface = (
            self.info_font.render(
                faction.name,
                True,
                (220, 220, 230)
            )
        )
        
        type_surface = (
            self.info_font.render(
                get_faction_type_label(
                    faction.faction_type
                ),
                True,
                (150, 150, 165)
            )
        )
        
        status_surface = (
            self.info_font.render(
                get_faction_status_label(
                    faction.status
                ),
                True,
                (150, 150, 165)
            )
        )
        
        screen.blit(
            name_surface,
            (300, y)
        )
        
        screen.blit(
            status_surface,
            (820, y)
        )
        
        