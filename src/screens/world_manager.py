import pygame

from src.ui.button import Button


class WorldManagerScreen:
    def __init__(
        self,
        app,
        world
    ):
        self.app = app
        self.world = world
        
        self.background_color = (
            30, 30, 35
        )
        
        self.title_font = pygame.font.Font(
            None, 48
        )
        
        self.name_font = pygame.font.Font(
            None, 34
        )
        
        self.info_font = pygame.font.Font(
            None, 24
        )
        
        self.back_button = Button(
            80, 110,
            220, 45,
            "← Biblioteca de Mundos"
        )
        
        self.regions = []
        
        self.scroll_offset = 0
        self.scroll_offset = 40
        
        self.list_rect = pygame.Rect(
            80, 315, 850, 335
        )
        
        self.refresh_regions()
        
    def refresh_regions(self):
        if self.world.id is None:
            self.regions = []
            return
        
        self.regions = (
            self.app
            .region_repository
            .get_all_by_world(
                self.world.id
            )
        )
    
    def handle_event(
        self,
        event
    ):
        if (
            event.type == pygame.KEYDOWN
            and event.type == pygame.K_ESCAPE
        ):
            self.app.open_world_library()
            return
        
        if self.back_button.handle_event(
            event
        ):
            self.app.open_world_library()
            return
        
        if event.type == pygame.MOUSEWHEEL:
            if self.list_rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.scroll_offset -= (
                    event.y * self.scroll_offset
                )
                
                self._clamp_scroll()
                
    def update(self):
        pass
    
    def render(
        self,
        screen
    ):
        screen.fill(
            self.background_color
        )
        
        title_surface = (
            self.info_font.render(
                "Gerenciar Mundo",
                True,
                (240, 240, 245)
            )
        )
        
        screen.blit(
            title_surface,
            (80, 50)
        )
        
        self.back_button.render(
            screen
        )
        
        world_surface = (
            self.name_font.render(
                self.world.name,
                True,
                (230, 220, 245)
            )
        )
        
        screen.blit(
            world_surface,
            (80, 180)
        )
        
        section_surface = (
            self.name_font.render(
                f"Regiões ({len(self.regions)})",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            section_surface,
            (80, 230)
        )
        
        self.render_regions(
            screen
        )
        
    def render_regions(
        self,
        screen
    ):
        if not self.regions:
            empty_surface = (
                self.info_font.render(
                    "Este mundo ainda não possui regiões.",
                    True,
                    (160, 160, 175)
                )
            )
            
            screen.blit(
                empty_surface,
                (80, 295)
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
        
        for region in self.regions:
            rect = pygame.Rect(
                80, y,
                760, 75
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                rect,
                border_radius=8
            )
            
            name_surface = (
                self.name_font.render(
                    region.name,
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
                region.description
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
            len(self.regions) * 90 - 5
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
