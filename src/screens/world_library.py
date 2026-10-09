import pygame

from enum import Enum, auto

from src.ui.button import Button
from src.ui.world.world_form import WorldForm


class WorldLibraryViewMode(Enum):
    LIST = auto()
    FORM = auto()
    
class WorldLibraryScreen:
    def __init__(
        self,
        app
    ):
        self.app = app
        
        self.background_color = (
            30,
            30,
            35
        )
        
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.name_font = pygame.font.Font(
            None,
            30
        )
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.view_mode = (
            WorldLibraryViewMode.LIST
        )
        
        self.form = WorldForm()
        
        self.worlds = (
            self.app
            .world_repository
            .get_all()
        )
        
        self.back_button = Button(
            80,
            110,
            160,
            45,
            "← Campanhas"
        )
        
        self.new_world_button = Button(
            260,
            110,
            180,
            45,
            "+ Novo Mundo"
        )
        
        self.world_card_rects = []
        
        self.scroll_offset = 0
        self.scroll_speed = 40
        
        self.list_rect = pygame.Rect(
            60,
            180,
            700,
            500
        )
        
    def handle_event(
        self,
        event
    ):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == WorldLibraryViewMode.FORM
            ):
                self.cancel_form()
                return
            
            self.app.open_campaigns()
            return
        
        if (
            self.view_mode
            == WorldLibraryViewMode.FORM
        ):
            self.handle_form_events(
                event
            )
            
            return
        
        self.handle_list_events(
            event
        )
        
    def handle_list_events(
        self,
        event
    ):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.list_rect.collidepoint(
                mouse_pos
            ):
                self.scroll_offset -= (
                    event.y
                    * self.scroll_speed
                )
                
                self._clamp_scroll()
                
                return
        
        if self.back_button.handle_event(
            event
        ):
            self.app.open_campaigns()
            return
        
        if self.new_world_button.handle_event(
            event
        ):
            self.form.prepare_create()
            
            self.view_mode = (
                WorldLibraryViewMode.FORM
            )
            
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if not self.list_rect.collidepoint(
                event.pos
            ):
                return
            
            for world, rect in self.world_card_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    self.app.open_world_manager(
                        world
                    )
                    
                    return
        
    def handle_form_events(
        self,
        event
    ):
        action = self.form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_form()
            return
        
        if action == "submit":
            self.create_world()
            return
        
    def create_world(self):
        world = self.form.build_world()
        
        if world is None:
            return
        
        self.app.world_repository.add(
            world
        )
        
        self.worlds.insert(
            0,
            world
        )
        
        self.scroll_offset = 0
        
        self.form.clear()
        
        self.view_mode = (
            WorldLibraryViewMode.LIST
        )
    
    def cancel_form(self):
        self.form.clear()
        
        self.view_mode = (
            WorldLibraryViewMode.LIST
        )
        
    def update(self):
        pass
    
    def render(
        self,
        screen
    ):
        screen.fill(
            self.background_color
        )
        
        if (
            self.view_mode
            == WorldLibraryViewMode.FORM
        ):
            self.form.render(
                screen
            )
            
            return
        
        self.render_list(
            screen
        )
        
    def render_list(
        self,
        screen
    ):
        title_surface = (
            self.title_font.render(
                "Gerenciar Mundos",
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
        
        self.new_world_button.render(
            screen
        )
        
        self.world_card_rects = []
        
        if not self.worlds:
            empty_surface = (
                self.info_font.render(
                    "Nenhum mundo canônico criado.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (80, 200)
            )
            
            return
        
        y = (
            190
            - self.scroll_offset
        )
        
        previous_clip = (
            screen.get_clip()
        )
        
        screen.set_clip(
            self.list_rect
        )
        
        for world in self.worlds:
            card_rect = pygame.Rect(
                80,
                y,
                620,
                90
            )
            
            self.world_card_rects.append(
                (
                    world,
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
                self.name_font.render(
                    world.name,
                    True,
                    (235, 235, 240)
                )
            )
            
            screen.blit(
                name_surface,
                (
                    card_rect.x + 20,
                    card_rect.y + 14
                )
            )
            
            description = (
                world.description
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
                    card_rect.x + 20,
                    card_rect.y + 52
                )
            )
            
            y += 110
            
        screen.set_clip(
            previous_clip
        )
        
    def _clamp_scroll(self):
        if not self.worlds:
            self.scroll_offset = 0
            return
        
        card_height = 90
        card_spacing = 20
        
        content_height = (
            len(self.worlds)
            * (
                card_height
                + card_spacing
            )
            - card_spacing
        )
        
        max_scroll = max(
            0,
            content_height
            - self.list_rect.height
        )
        
        self.scroll_offset = max(
            0,
            min(
                self.scroll_offset,
                max_scroll
            )
        )
