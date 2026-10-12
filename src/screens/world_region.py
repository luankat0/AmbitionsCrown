import pygame

from enum import Enum, auto

from src.ui.button import Button
from src.ui.location.location_form import (
    LocationForm,
)

class WorldRegionViewMode(Enum):
    DETAILS = auto()
    LOCATION_FORM = auto()


class WorldRegionScreen:
    def __init__(
        self,
        app,
        world,
        region
    ):
        self.app = app
        self.world = world
        self.region = region
        
        self.background_color = (
            30, 30, 35
        )
        
        self.title_font = pygame.font.Font(
            None, 48
        )
        
        self.name_font = pygame.font.Font(
            None, 32
        )
        
        self.info_font = pygame.font.Font(
            None, 24
        )
        
        self.back_button = Button(
            80, 110,
            220, 45,
            "← Voltar ao Mundo"
        )
        
        self.view_mode = WorldRegionViewMode.DETAILS
        
        self.location_form = LocationForm()
        
        self.new_location_button = Button(
            650,
            285,
            190,
            45,
            "+ Novo Local"
        )
        
        self.locations = []
        self.location_card_rects = []
        
        self.list_rect = pygame.Rect(
            80, 330, 850, 320
        )
        
        self.scroll_offset = 0
        self.scroll_speed = 40
        
        self.refresh_locations()
        
    def refresh_locations(self):
        if self.region.id is None:
            self.locations = []
            return
        
        locations = (
            self.app
            .location_repository
            .get_all_by_region(
                self.region.id
            )
        )
        
        self.locations = [
            location
            for location in locations
            if location.parent_location_id is None
        ]
        
    def handle_event(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == WorldRegionViewMode.LOCATION_FORM
            ):
                self.cancel_location_form()
                return
            
            self.return_to_world()
            return
        
        if (
            self.view_mode
            == WorldRegionViewMode.LOCATION_FORM
        ):
            self.handle_location_form_events(
                event
            )
            return
        
        if self.back_button.handle_event(event):
            self.return_to_world()
            return
        
        if self.new_location_button.handle_event(event):
            self.location_form.prepare_create()
            
            self.view_mode = (
                WorldRegionViewMode.LOCATION_FORM
            )
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.list_rect.collidepoint(event.pos):
                for location, rect in self.location_card_rects:
                    if rect.collidepoint(event.pos):
                        self.app.open_world_location(
                            self.world,
                            self.region,
                            location
                        )
                        return
        
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
        screen.fill(
            self.background_color
        )
        
        if (
            self.view_mode
            == WorldRegionViewMode.LOCATION_FORM
        ):
            self.location_form.render(
                screen
            )
            return
        
        title_surface = (
            self.title_font.render(
                "Gerenciar Região",
                True,
                (240, 240, 245)
            )
        )
        
        screen.blit(
            title_surface,
            (80, 55)
        )
        
        self.back_button.render(
            screen
        )
        
        self.new_location_button.render(
            screen
        )
        
        region_surface = (
            self.title_font.render(
                self.region.name,
                True,
                (230, 220, 245)
            )
        )
        
        screen.blit(
            region_surface,
            (80, 180)
        )
        
        description = (
            self.region.description
            or "Sem descrição."
        )
        
        description_surface = (
            self.info_font.render(
                description,
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            description_surface,
            (80, 235)
        )
        
        section_surface = (
            self.name_font.render(
                f"Locais ({len(self.locations)})",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            section_surface,
            (80, 290)
        )
        
        self.render_locations(
            screen
        )
        
    def render_locations(self, screen):
        self.location_card_rects = []
        
        if not self.locations:
            empty_surface = (
                self.info_font.render(
                    "Esta região não possui locais.",
                    True,
                    (160, 160, 175)
                )
            )
            
            screen.blit(
                empty_surface,
                (80, 345)
            )
            
            return
        
        self._clamp_scroll()
        
        previous_clip = screen.get_clip()
        
        screen.set_clip(
            self.list_rect
        )
        
        y = (
            self.list_rect.y
            + 10
            - self.scroll_offset
        )
        
        for location in self.locations:
            rect = pygame.Rect(
                80, y,
                760, 75
            )
            
            self.location_card_rects.append(
                (location, rect)
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                rect,
                border_radius=8
            )
            
            name_surface = (
                self.name_font.render(
                    location.name,
                    True,
                    (235, 235, 240)
                )
            )
            
            screen.blit(
                name_surface,
                (
                    rect.x + 20,
                    rect.y + 10
                )
            )
            
            description = (
                location.description
                or "Sem descrição."
            )
            
            description_surface = (
                self.info_font.render(
                    description,
                    True,
                    (155, 155, 165)
                )
            )
            
            screen.blit(
                description_surface,
                (
                    rect.x + 20,
                    rect.y + 45
                )
            )
            
            y += 90
        
        screen.set_clip(
            previous_clip
        )
        
    def _clamp_scroll(self):
        content_height = max(
            0,
            len(self.locations) * 90 - 5
        )
        
        max_scroll = max(
            0,
            content_height - self.list_rect.height
        )
        
        self.scroll_offset = max(
            0,
            min(
                self.scroll_offset,
                max_scroll
            )
        )
        
    def handle_location_form_events(self, event):
        action = self.location_form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_location_form()
            return
        
        if action == "submit":
            self.create_location()
            return
        
    def cancel_location_form(self):
        self.location_form.clear()
        
        self.view_mode = (
            WorldRegionViewMode.DETAILS
        )
        
    def create_location(self):
        if self.region.id is None:
            return
        
        location = (
            self.location_form.build_location(
                region_id=self.region.id,
                parent_location_id=None
            )
        )
        
        if location is None:
            return
        
        self.app.location_repository.add(
            location
        )
        
        self.refresh_locations()
        
        self.scroll_offset = 0
        
        self.location_form.clear()
        
        self.view_mode = (
            WorldRegionViewMode.DETAILS
        )
