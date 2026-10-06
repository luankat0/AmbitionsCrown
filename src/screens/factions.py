import pygame

from enum import Enum, auto

from src.ui.faction.faction_form import FactionForm

from src.screens.base_screen import BaseScreen
from src.ui.button import Button


class FactionViewMode(Enum):
    LIST = auto()
    FORM = auto()

class FactionScreen(BaseScreen):
    def __init__(
        self,
        app
    ):
        super().__init__(
            app,
            "factions"
        )
        
        self.view_mode = (
            FactionViewMode.LIST
        )
        
        self.faction_form = FactionForm()
        
        self.new_faction_button = Button(
            300,
            160,
            180,
            45,
            "+ Nova Facção"
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
        
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if self.view_mode == FactionViewMode.FORM:
                self.cancel_faction_form()
                return
            
        if self.view_mode == FactionViewMode.FORM:
            self.handle_faction_form_events(
                event
            )
            return
        
        if self.new_faction_button.handle_event(
            event
        ):
            self.faction_form.prepare_create()
            
            self.view_mode = (
                FactionViewMode.FORM
            )
            
            return
       
    def handle_faction_form_events(
        self,
        event
    ):
        action = (
            self.faction_form.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.cancel_faction_form()
            return
        
        if action == "submit":
            self.create_faction()
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
        
        if self.view_mode == FactionViewMode.FORM:
            self.faction_form.render(
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
        self.new_faction_button.render(
            screen
        )
        
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
                (300, 240)
            )
            
            return
    
        y = 240
    
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

    def cancel_faction_form(self):
        self.faction_form.clear()
        
        self.view_mode = (
            FactionViewMode.LIST
        )
        
    def create_faction(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.world_id is None
        ):
            return
        
        faction = (
            self.faction_form.build_faction(
                campaign.world_id
            )
        )
        
        if faction is None:
            return
        
        self.app.faction_repository.add(
            faction
        )
        
        self.refresh_factions()
        
        self.faction_form.clear()
        
        self.view_mode = (
            FactionViewMode.LIST
        )

