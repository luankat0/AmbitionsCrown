import pygame

from enum import Enum, auto

from src.ui.button import Button

from src.ui.faction.faction_labels import (
    get_faction_type_label,
    get_faction_status_label,
)
from src.ui.faction.faction_form import (
    FactionForm,
)

class WorldFactionsViewMode(Enum):
    LIST = auto()
    FORM = auto()


class WorldFactionsScreen:
    def __init__(self, app, world):
        self.app = app
        self.world = world

        self.background_color = (30, 30, 35)

        self.title_font = pygame.font.Font(None, 48)
        self.name_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)

        self.back_button = Button(
            80, 110,
            220, 45,
            "Voltar ao Mundo"
        )
        
        self.view_mode = WorldFactionsViewMode.LIST
        
        self.faction_form = FactionForm()
        
        self.new_faction_button = Button(
            650, 240,
            190, 45,
            "+ Nova Facção"
        )

        self.list_rect = pygame.Rect(
            80, 290, 850, 360
        )

        self.scroll_offset = 0
        self.scroll_speed = 40

        self.factions = []

        self.refresh_factions()

    def refresh_factions(self):
        if self.world.id is None:
            self.factions = []
            return

        self.factions = (
            self.app.faction_repository.get_all_by_world(
                self.world.id
            )
        )

        self._clamp_scroll()

    def handle_event(self, event):
        
        # Eventos de ESC
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == WorldFactionsViewMode.FORM
            ):
                self.cancel_faction_form()
                return
            
            self.return_to_world()
            return
        
        # Eventos do Formulário
        if (
            self.view_mode
            == WorldFactionsViewMode.FORM
        ):
            self.handle_faction_form_events(event)
            return
        
        # Voltar ao World
        if self.back_button.handle_event(event):
            self.return_to_world()
            return

        # Criar facção
        if self.new_faction_button.handle_event(event):
            self.faction_form.prepare_create()
            
            self.view_mode = (
                WorldFactionsViewMode.FORM
            )
            return
            
        # Scroll da lista
        if event.type == pygame.MOUSEWHEEL:
            if self.list_rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.scroll_offset -= (
                    event.y * self.scroll_speed
                )

                self._clamp_scroll()

    def return_to_world(self):
        self.app.open_world_manager(
            self.world
        )

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.background_color)
        
        if (
            self.view_mode
            == WorldFactionsViewMode.FORM
        ):
            self.faction_form.render(screen)
            return

        title = self.title_font.render(
            "Facções do Mundo",
            True,
            (240, 240, 245)
        )

        screen.blit(title, (80, 55))

        self.back_button.render(screen)
        
        self.new_faction_button.render(screen)

        world_name = self.name_font.render(
            self.world.name,
            True,
            (200, 180, 225)
        )

        screen.blit(world_name, (80, 190))

        section = self.name_font.render(
            f"Facções ({len(self.factions)})",
            True,
            (235, 235, 240)
        )

        screen.blit(section, (80, 250))

        self.render_factions(screen)

    def render_factions(self, screen):
        if not self.factions:
            message = self.info_font.render(
                "Este mundo ainda não possui facções.",
                True,
                (160, 160, 175)
            )

            screen.blit(message, (80, 315))
            return

        self._clamp_scroll()

        previous_clip = screen.get_clip()
        screen.set_clip(self.list_rect)

        y = (
            self.list_rect.y
            + 10
            - self.scroll_offset
        )

        for faction in self.factions:
            rect = pygame.Rect(
                80, y,
                760, 95
            )

            pygame.draw.rect(
                screen,
                (45, 45, 55),
                rect,
                border_radius=8
            )

            name = self.name_font.render(
                faction.name,
                True,
                (235, 235, 240)
            )

            screen.blit(
                name,
                (rect.x + 20, rect.y + 15)
            )

            faction_type = get_faction_type_label(
                faction.faction_type
            )

            faction_status = get_faction_status_label(
                faction.status
            )

            details = self.info_font.render(
                f"{faction_type} | {faction_status}",
                True,
                (165, 150, 185)
            )

            screen.blit(
                details,
                (rect.x + 20, rect.y + 55)
            )

            y += 108

        screen.set_clip(previous_clip)

    def _clamp_scroll(self):
        if not self.factions:
            self.scroll_offset = 0
            return

        content_height = (
            10
            + (len(self.factions) - 1) * 108
            + 95
        )

        max_scroll = max(
            0,
            content_height - self.list_rect.height
        )

        self.scroll_offset = max(
            0,
            min(self.scroll_offset, max_scroll)
        )

    def handle_faction_form_events(self, event):
        action = self.faction_form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_faction_form()
            return
        
        if action == "submit":
            self.create_faction()
            return
        
    def cancel_faction_form(self):
        self.faction_form.clear()
        
        self.view_mode = (
            WorldFactionsViewMode.LIST
        )
    
    def create_faction(self):
        if self.world.id is None:
            return
        
        faction = self.faction_form.build_faction(
            self.world.id
        )
        
        if faction is None:
            return
        
        self.app.faction_repository.add(
            faction
        )
        
        self.refresh_factions()
        
        self.scroll_offset = 0
        
        self.faction_form.clear()
        
        self.view_mode = (
            WorldFactionsViewMode.LIST
        )
