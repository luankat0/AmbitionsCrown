import pygame

from src.screens.base_screen import BaseScreen
from src.ui.button import Button


class FactionScreen(BaseScreen):
    def __init__(
        self,
        app
    ):
        super().__init__(
            app,
            "factions"
        )
        
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.factions = []
        
        self.go_to_world_button = Button(
            300,
            260,
            180,
            45,
            "Ir para Mundo"
        )
        
        self.refresh_factions()
        
    def refresh_factions(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.world_id is None
        ):
            self.factions = []
            return
        
        self.factions = (
            self.app
            .faction_repository
            .get_all_by_world(
                campaign.world_id
            )
        )
        
    def handle_event(
        self,
        event
    ):
        super().handle_event(
            event
        )
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        if campaign.world_id is None:
            if self.go_to_world_button.handle_event(
                event
            ):
                self.app.open_world()
            
            return
        
    def update(self):
        pass
    
    def render(
        self,
        screen
    ):
        super().render(
            screen
        )
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
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
        
        if campaign.world_id is None:
            self.render_without_world(
                screen
            )
            return
        
        self.render_factions(
            screen
        )
        
    def render_without_world(
        self,
        screen
    ):
        message_surface = (
            self.info_font.render(
                (
                    "Esta campanha ainda não "
                    "possui um mundo associado."
                ),
                True,
                (190, 190, 200)
            )
        )
        
        explanation_surface = (
            self.info_font.render(
                (
                    "As facções pertencem "
                    "ao mundo."
                ),
                True,
                (150, 150, 165)
            )
        )
        screen.blit(
            message_surface,
            (300, 175)
        )
        
        screen.blit(
            explanation_surface,
            (300, 210)
        )
        
        self.go_to_world_button.render(
            screen
        )
        
    def render_factions(
        self,
        screen
    ):
        if not self.factions:
            empty_surface = (
                self.info_font.render(
                    "Nenhuma facção criada ainda.",
                    True,
                    (150, 150, 160)
                )
            )
        
            screen.blit(
                empty_surface,
                (300, 175)
            )
            
            return
    
        y = 175
    
        for faction in self.factions:
            name_surface = (
                self.info_font.render(
                    faction.name,
                    True,
                    (220, 220, 230)
                )
            )
            
            screen.blit(
                name_surface,
                (300, y)
            )
            
            y += 40