import pygame

from enum import Enum, auto

from src.ui.button import Button
from src.ui.dialogs.confirm_dialog import ConfirmDialog

from src.ui.faction.faction_form import FactionForm
from src.ui.faction.faction_list_view import FactionListView
from src.ui.faction.faction_details_view import FactionDetailsView

from src.screens.base_screen import BaseScreen


class FactionViewMode(Enum):
    LIST = auto()
    DETAILS = auto()
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
        
        self.confirm_dialog = ConfirmDialog()
        
        self.faction_form = FactionForm()
        self.list_view = FactionListView()
        self.details_view = FactionDetailsView()
        
        self.selected_faction = None
        
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
        if self.confirm_dialog.visible:
            action = self.confirm_dialog.handle_event(
                event
            )
            
            if action == "cancel":
                self.confirm_dialog.close()
                return
            
            if action == "confirm":
                self.confirm_delete_faction()
                return
            
            return
        
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
            
            if self.view_mode == FactionViewMode.DETAILS:
                self.return_to_list()
                return
            
        if self.view_mode == FactionViewMode.FORM:
            self.handle_faction_form_events(
                event
            )
            return
        
        if self.view_mode == FactionViewMode.DETAILS:
            self.handle_details_events(
                event
            )
        
        self.handle_list_events(
            event
        )
        
    def handle_list_events(
        self,
        event
    ):
        action, faction = (
            self.list_view.handle_event(
                event
            )
        )
        
        if action == "new":
            self.faction_form.prepare_create()
            
            self.view_mode = (
                FactionViewMode.FORM
            )
            
            return
        
        if (
            action == "select"
            and faction is not None
        ):
            self.selected_faction = faction
            
            self.view_mode = (
                FactionViewMode.DETAILS
            )  
            
            return
    
    def handle_details_events(
        self,
        event
    ):
        action, _ = (
            self.details_view.handle_event(
                event
            )
        )
        
        if action == "back":
            self.return_to_list()
            return
        
        if action == "edit":
            if self.selected_faction is None:
                return
            
            self.faction_form.prepare_edit(
                self.selected_faction
            )
            
            self.view_mode = (
                FactionViewMode.FORM
            )
            
            return
        
        if action == "delete":
            self.request_delete_faction()
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
            self.save_faction()
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
        
        if campaign.world_id is None:
            self.render_without_world(
                screen
            )
        
        elif self.view_mode == FactionViewMode.FORM:
            self.faction_form.render(
                screen
            )
        
        elif self.view_mode == FactionViewMode.DETAILS:
            if self.selected_faction is None:
                self.return_to_list()
                
                self.list_view.render(
                    screen,
                    self.factions
                )
            else:
                self.details_view.render(
                    screen,
                    self.selected_faction
                )
        else:
            self.list_view.render(
                screen,
                self.factions
            )
        
        if self.confirm_dialog.visible:
            self.confirm_dialog.render(
                screen
            )
        
    def render_without_world(
        self,
        screen
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
        
    def cancel_faction_form(self):
        is_editing = (
            self.faction_form.editing_faction_id
            is not None
        )        
        
        self.faction_form.clear()
        self.faction_form.editing_faction_id = None
        
        if (
            is_editing
            and self.selected_faction is not None
        ):
            self.view_mode = (
                FactionViewMode.DETAILS
            )
            return
        
        self.selected_faction = None
        
        self.view_mode = (
            FactionViewMode.LIST
        )
        
    def save_faction(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.world_id is None
        ):
            return
        
        is_editing = (
            self.faction_form.editing_faction_id
            is not None
        )
        
        if is_editing:
            if self.selected_faction is None:
                return
            
            world_id = (
                self.selected_faction.world_id
            )
        else:
            world_id = campaign.world_id
            
        faction = (
            self.faction_form.build_faction(
                world_id
            )
        )
            
        if faction is None:
            return
            
        if is_editing:
            self.app.faction_repository.update(
                faction
            )
            
            self.refresh_factions()
            
            self.selected_faction = (
                self.app
                .faction_repository
                .get_by_id(
                    faction.id
                )
            )
            
            self.faction_form.clear()
            self.faction_form.editing_faction_id = None
            
            self.view_mode = (
                FactionViewMode.DETAILS
            )
            
            return
        
        self.app.faction_repository.add(
            faction
        )
        
        self.refresh_factions()
        
        self.faction_form.clear()
        
        self.view_mode = (
            FactionViewMode.LIST
        )

    def return_to_list(self):
        self.selected_faction = None
        
        self.view_mode = (
            FactionViewMode.LIST
        )

    def request_delete_faction(self):
        if self.selected_faction is None:
            return
        
        self.confirm_dialog.open(
            title="Excluir Facção",
            message=(
                f"Excluir '{self.selected_faction.name}'?"
            ),
            warning=(
                "Esta ação não pode ser desfeita."
            ),
            confirm_text="Excluir"
        )
        
    def confirm_delete_faction(self):
        if self.selected_faction is None:
            self.confirm_dialog.close()
            return
        
        faction = self.selected_faction
        
        self.confirm_dialog.close()
        
        self.app.faction_repository.delete(
            faction
        )
        
        self.selected_faction = None
        
        self.refresh_factions()
        
        self.view_mode = (
            FactionViewMode.LIST
        )

