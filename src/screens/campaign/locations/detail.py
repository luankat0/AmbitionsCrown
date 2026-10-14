import pygame

from enum import Enum, auto

from src.screens.base_screen import BaseScreen

from src.ui.location.location_details_view import LocationDetailsView
from src.ui.location.location_form import LocationForm

from src.ui.dialogs.confirm_dialog import ConfirmDialog
from src.ui.dialogs.message_dialog import MessageDialog

class LocationViewMode(Enum):
    DETAILS = auto()
    EDIT_FORM = auto()
    CHILD_FORM = auto()


class LocationScreen(BaseScreen):
    def __init__(
        self,
        app,
        region,
        location
    ):
        super().__init__(
            app,
            "world"
        )
        
        self.region = region
        self.location = location
        
        self.children = []
        
        
        self.details_view = (
            LocationDetailsView()
        )
        
        self.location_form = LocationForm()
        
        self.view_mode = (
            LocationViewMode.DETAILS
        )
        
        self.refresh_children()
        
        self.confirm_dialog = ConfirmDialog()
        self.message_dialog = MessageDialog(
            "",
            ""
        )
        
    def handle_event(
        self,
        event
    ):
        if self.message_dialog.visible:
            self.message_dialog.handle_event(
                event
            )
            return
        
        if self.confirm_dialog.visible:
            action = (
                self.confirm_dialog
                .handle_event(
                    event
                )
            )
            
            if action == "cancel":
                self.confirm_dialog.close()
                return
            
            if action == "confirm":
                self.confirm_delete_location()
                return
            
            return
            
        super().handle_event(
            event
        )
        
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if self.view_mode in (
                LocationViewMode.EDIT_FORM,
                LocationViewMode.CHILD_FORM
            ):
                self.cancel_location_form()
                return
            
            self.navigate_back()
            return
        
        if (
            self.view_mode
            == LocationViewMode.EDIT_FORM
        ):
            self.handle_edit_form_events(
                event
            )
            return
        
        if (
            self.view_mode
            == LocationViewMode.CHILD_FORM
        ):
            self.handle_child_form_events(
                event
            )
            return
        
        self.handle_details_events(
            event
        )
        
    def handle_details_events(
        self,
        event
    ):
        action, child = (
            self.details_view.handle_event(
                event
            )
        )
        
        if action == "back":
            self.navigate_back()
            return
        
        if action == "edit_location":
            self.location_form.prepare_edit(
                self.location
            )
            
            self.view_mode = (
                LocationViewMode.EDIT_FORM
            )
            
            return
        
        if action == "delete_location":
            self.request_delete_location()
            return
        
        if action == "new_child":
            self.location_form.prepare_create()
            
            self.view_mode = (
                LocationViewMode.CHILD_FORM
            )
            
            return
        
        if (
            action == "open_child"
            and child is not None
        ):
            self.open_child(
                child
            )
            
            return
        
    def handle_child_form_events(
        self,
        event
    ):
        action = (
            self.location_form.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.cancel_location_form()
            return
        
        if action == "submit":
            self.create_child()
            return
        
    def cancel_location_form(self):
        self.location_form.clear()
        
        self.view_mode = (
            LocationViewMode.DETAILS
        )
        
    def create_child(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.id is None
            or self.region.id is None
            or self.location.id is None
        ):
            return
        
        child = (
            self.location_form
            .build_campaign_location(
                campaign_id=campaign.id,
                region_id=self.region.id,
                parent_location_id=(
                    self.location.id
                )
            )
        )
        
        if child is None:
            return
        
        self.app.campaign_location_repository.add(
            child
        )
        
        self.refresh_children()
        
        self.location_form.clear()
        
        self.view_mode = (
            LocationViewMode.DETAILS
        )
        
    def return_to_region(self):
        self.app.open_region(
            self.region
        )
        
    def update(self):
        pass
    
    def render(
        self,
        screen
    ):
        super().render(
            screen
        )
        
        if self.view_mode in (
            LocationViewMode.EDIT_FORM,
            LocationViewMode.CHILD_FORM,
        ):
            self.location_form.render(
                screen
            )
        
        else:
            self.details_view.render(
                screen,
                self.location,
                self.children
            )
        
        self.message_dialog.render(
            screen
        )
        
        self.confirm_dialog.render(
            screen
        )
        
    def refresh_children(self):
        if self.location.id is None:
            self.children = []
            return
        
        self.children = (
            self.app
            .campaign_location_repository
            .get_children(
                self.location.id
            )
        )

    def open_child(
        self,
        child
    ):
        self.app.open_location(
            self.region,
            child
        )
        
    def navigate_back(self):
        parent_id = (
            self.location
            .parent_location_id
        )
        
        if parent_id is None:
            self.return_to_region()
            return

        parent = (
            self.app
            .campaign_location_repository
            .get_by_id(
                parent_id
            )
        )
        
        if parent is None:
            self.return_to_region()
            return
        
        self.app.open_location(
            self.region,
            parent
        )

    def handle_edit_form_events(
        self,
        event
    ):
        action = (
            self.location_form.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.cancel_location_form()
            return
        
        if action == "submit":
            self.update_location()
            return
        
    def update_location(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.id is None
            or self.location.id is None
        ):
            return
        
        updated_location = (
            self.location_form
            .build_campaign_location(
                campaign_id=campaign.id,
                region_id=self.location.region_id,
                parent_location_id=(
                    self.location
                    .parent_location_id
                )
            )
        )
        
        if updated_location is None:
            return
        
        updated_location.id = (
            self.location.id
        )
        
        updated_location.source_location_id = (
            self.location.source_location_id
        )
        
        self.app.campaign_location_repository.update(
            updated_location
        )
        
        refreshed_location = (
            self.app
            .campaign_location_repository
            .get_by_id(
                updated_location.id
            )
        )
        
        if refreshed_location is not None:
            self.location = refreshed_location
        else:
            self.location = updated_location
        
        self.refresh_children()
        
        self.location_form.clear()
        
        self.view_mode = (
            LocationViewMode.DETAILS
        )

    def request_delete_location(self):
        if self.location.id is None:
            return
        
        children = (
            self.app
            .campaign_location_repository
            .get_children(
                self.location.id
            )
        )
        
        if children:
            child_count = len(
                children
            )
            
            child_label = (
                "sublocal"
                if child_count == 1
                else "sublocais"
            )
            
            self.message_dialog.set_message(
                "Não é possível excluir",
                (
                    f'"{self.location.name}" possui '
                    f"{child_count} {child_label}."
                )
            )
            
            self.message_dialog.open()
            return
        
        self.confirm_dialog.open(
            "Excluir local?",
            (
                f'Tem certeza que deseja excluir '
                f'"{self.location.name}"?'
            ),
            "Esta ação não pode ser desfeita.",
            "Excluir"
        )

    def confirm_delete_location(self):
        parent_id = (
            self.location
            .parent_location_id
        )
        
        self.confirm_dialog.close()
        
        try:
            self.app.campaign_location_repository.delete(
                self.location
            )
        
        except ValueError as error:
            self.message_dialog.set_message(
                "Não é possível excluir",
                str(error)
            )
            
            self.message_dialog.open()
            return
        
        if parent_id is None:
            self.return_to_region()
            return
        
        parent = (
            self.app
            .campaign_location_repository
            .get_by_id(
                parent_id
            )
        )
        
        if parent is None:
            self.return_to_region()
            return
        
        self.app.open_location(
            self.region,
            parent
        )

