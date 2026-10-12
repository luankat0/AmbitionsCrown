import pygame

from enum import Enum, auto

from src.ui.button import Button

from src.ui.location.location_form import (
    LocationForm,
)

class WorldLocationViewMode(Enum):
    DETAILS = auto()
    CHILD_FORM = auto()
    EDIT_FORM = auto()

class WorldLocationScreen:
    def __init__(
        self,
        app,
        world,
        region,
        location
    ):
        self.app = app
        self.world = world
        self.region = region
        self.location = location
        
        self.background_color = (30, 30, 35)
        
        self.title_font = pygame.font.Font(None, 48)
        self.name_font = pygame.font.Font(None, 32)
        self.info_font = pygame.font.Font(None, 24)
        
        self.back_button = Button(
            80, 110, 180, 45,
            "← Voltar"
        )
        
        self.view_mode = (
            WorldLocationViewMode.DETAILS
        )
        
        self.location_form = LocationForm()
        
        self.new_child_button = Button(
            650,
            285,
            190,
            45,
            "+ Novo Sublocal"
        )
        
        self.edit_button = Button(
            440,
            285,
            185,
            45,
            "Editar Local"
        )
        
        self.children = []
        self.child_card_rects = []
        
        self.list_rect = pygame.Rect(
            80, 330, 850, 320
        )
        
        self.scroll_offset = 0
        self.scroll_speed = 40
        
        self.refresh_children()
        
    def refresh_children(self):
        if self.location.id is None:
            self.children = []
            return
        
        self.children = (
            self.app.location_repository.get_children(
                self.location.id
            )
        )
        
        self._clamp_scroll()
        
    def navigate_back(self):
        parent_id = self.location.parent_location_id
        
        if parent_id is None:
            self.app.open_world_region(
                self.world,
                self.region,
            )
            return
        
        parent = (
            self.app.location_repository.get_by_id(
                parent_id
            )
        )
        
        if parent is None:
            self.app.open_world_region(
                self.world,
                self.region
            )
            return
        
        self.app.open_world_location(
            self.world,
            self.region,
            parent
        )
        
    def handle_event(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if self.view_mode in (
                WorldLocationViewMode.CHILD_FORM,
                WorldLocationViewMode.EDIT_FORM
            ):
                self.cancel_child_form()
                return
            
            self.navigate_back()
            return
        
        if (
            self.view_mode
            == WorldLocationViewMode.EDIT_FORM
        ):
            self.handle_edit_form_events(event)
            return
        
        if (
            self.view_mode
            == WorldLocationViewMode.CHILD_FORM
        ):
            self.handle_child_form_events(event)
            return
        
        if self.back_button.handle_event(event):
            self.navigate_back()
            return
        
        if self.edit_button.handle_event(event):
            self.location_form.prepare_edit(
                self.location
            )
            
            self.view_mode = (
                WorldLocationViewMode.EDIT_FORM
            )
            
            return
        
        if self.new_child_button.handle_event(event):
            self.location_form.prepare_create()
            
            self.view_mode = (
                WorldLocationViewMode.CHILD_FORM
            )
            
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.list_rect.collidepoint(event.pos):
                for child, rect in self.child_card_rects:
                    if rect.collidepoint(event.pos):
                        self.app.open_world_location(
                            self.world,
                            self.region,
                            child
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
    
    def handle_child_form_events(self, event):
        action = self.location_form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_child_form()
            return
        
        if action == "submit":
            self.create_child()
            return
    
    def handle_edit_form_events(self, event):
        action = self.location_form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_child_form()
            return
        
        if action == "submit":
            self.update_location()
            return
    
    def create_child(self):
        if (
            self.region.id is None
            or self.location.id is None
        ):
            return
        
        child = (
            self.location_form.build_location(
                region_id=self.region.id,
                parent_location_id=self.location.id
            )
        )
        
        if child is None:
            return
        
        self.app.location_repository.add(
            child
        )
        
        self.refresh_children()
        
        self.scroll_offset = 0
        
        self.location_form.clear()
        
        self.view_mode = (
            WorldLocationViewMode.DETAILS
        )
    
    def update(self):
        pass
    
    def update_location(self):
        if self.location.id is None:
            return
        
        updated_location = (
            self.location_form.build_location(
                region_id=self.location.region_id,
                parent_location_id=(
                    self.location.parent_location_id
                )
            )
        )
        
        if updated_location is None:
            return
        
        updated_location.id = self.location.id
        
        self.app.location_repository.update(
            updated_location
        )
        
        refreshed_location = (
            self.app
            .location_repository
            .get_by_id(
                self.location.id
            )
        )
        
        if refreshed_location is not None:
            self.location = refreshed_location
            
        self.location_form.clear()
        
        self.view_mode = (
            WorldLocationViewMode.DETAILS
        )
    
    def render(self, screen):
        screen.fill(self.background_color)
        
        if self.view_mode in (
            WorldLocationViewMode.CHILD_FORM,
            WorldLocationViewMode.EDIT_FORM
        ):
            self.location_form.render(screen)
            return
        
        title = self.title_font.render(
            "Gerenciar Local",
            True,
            (240, 240, 245)
        )
        
        screen.blit(title, (80, 55))
        
        self.back_button.render(screen)
        
        self.edit_button.render(screen)
        
        self.new_child_button.render(
            screen
        )
        
        name = self.title_font.render(
            self.location.name,
            True,
            (230, 220, 245)
        )
        
        screen.blit(name, (80, 180))
        
        description = (
            self.location.description
            or "Sem descrição"
        )
        
        description_surface = self.info_font.render(
            description,
            True,
            (160, 160, 175)
        )
        
        screen.blit(
            description_surface,
            (80, 235)
        )
        
        section = self.name_font.render(
            f"Sublocais ({len(self.children)})",
            True,
            (235, 235, 240)
        )
        
        screen.blit(section, (80, 290))
        
        self.render_children(screen)
        
    def render_children(self, screen):
        self.child_card_rects = []
        
        if not self.children:
            message = self.info_font.render(
                "Este local não possui sublocais.",
                True,
                (160, 160, 175)
            )
            
            screen.blit(message, (80, 345))
            return
        
        self._clamp_scroll()
        
        previous_clip = screen.get_clip()
        screen.set_clip(self.list_rect)
        
        y = (
            self.list_rect.y
            + 10
            - self.scroll_offset
        )
        
        for child in self.children:
            rect = pygame.Rect(
                80, y, 760, 75
            )
            
            self.child_card_rects.append(
                (child, rect)
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                rect,
                border_radius=8
            )
            
            name = self.name_font.render(
                child.name,
                True,
                (235, 235, 240)
            )
            
            screen.blit(
                name,
                (rect.x + 20, rect.y + 10)
            )
            
            description = (
                child.description
                or "Sem descrição."
            )
            
            info = self.info_font.render(
                description,
                True,
                (155, 155, 165)
            )
            
            screen.blit(
                info,
                (rect.x + 20, rect.y + 45)
            )
            
            y += 90
            
        screen.set_clip(previous_clip)
        
    def _clamp_scroll(self):
        content_height = max(
            0,
            len(self.children) * 90 - 5
        )
        
        max_scroll = max(
            0,
            content_height - self.list_rect.height
        )
        
        self.scroll_offset = max(
            0,
            min(self.scroll_offset, max_scroll)
        )

    def cancel_child_form(self):
        self.location_form.clear()
        
        self.view_mode = (
            WorldLocationViewMode.DETAILS
        )
