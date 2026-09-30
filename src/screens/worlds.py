import pygame

from src.ui.button import Button

from src.screens.base_screen import BaseScreen

class WorldScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(
            app,
            "world"
        )
                
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.name_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None, 
            24
        )
        
        self.background_color = (
            30,
            30,
            35
        )
        
        self.worlds = (
            self.app
            .world_repository
            .get_all()
        )
        
        self.world_card_rects = {}
        
        self.change_world_button = Button(
            300,
            200,
            180,
            45,
            "Trocar Mundo"
        )
        
        self.selecting_world = False
        
    def handle_event(self, event):
        super().handle_event(event)
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        if (
            campaign.world_id is not None
            and not self.selecting_world
        ):
            if self.change_world_button.handle_event(
                event
            ):
                self.selecting_world = True
            
            return
        
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if campaign.world_id is not None:
                self.selecting_world = False
                
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for world, rect in self.world_card_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    self.select_world(
                        world
                    )
                    
                    return
    
    def update(self):
        pass
    
    def render(self, screen):
        super().render(
            screen
        )
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        title = self.title_font.render(
            "Mundo",
            True,
            (240, 240, 245)
        )
        
        screen.blit(
            title,
            (300, 50)
        )
        
        if (
            campaign.world_id is not None
            and not self.selecting_world
        ):
            self.render_current_world(
                screen
            )
        else:
            self.render_world_selection(
                screen
            )
            
    def render_current_world(
        self, 
        screen
    ):
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        if campaign.world_id is None:
            return
        
        world = (
            self.app
            .world_repository
            .get_by_id(
                campaign.world_id
            )
        )
        
        if world is None:
            missing_surface = (
                self.info_font.render(
                    "O mundo associado não foi encontrado.",
                    True,
                    (200, 90, 100)
                )
            )
            
            screen.blit(
                missing_surface,
                (300, 130)
            )
            
            return
        
        label_surface = (
            self.info_font.render(
                "Mundo da campanha",
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            label_surface,
            (300, 120)
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
            (300, 155)
        )
        
        self.change_world_button.render(
            screen
        )
        
    def render_world_selection(
        self,
        screen
    ):
        info_surface = (
            self.info_font.render(
                "Selecione um mundo para esta campanha:",
                True,
                (180, 180, 195)
            )
        )
        
        screen.blit(
            info_surface,
            (300, 120)
        )
        
        self.world_card_rects = []
        
        if not self.worlds:
            empty_surface = (
                self.info_font.render(
                    "Nenhum mundo criado ainda.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (300, 180)
            )
            
            return
        
        y = 180
        
        for world in self.worlds:
            card_rect = pygame.Rect(
                300,
                y,
                600,
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
                    card_rect.y + 15
                )
            )
            
            description = world.description
            
            if not description:
                description = (
                    "Sem descrição."
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
            
    def select_world(
        self,
        world
    ):
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        campaign.world_id = world.id
        
        self.app.campaign_repository.update(
            campaign
        )
        
        self.selecting_world = False
        