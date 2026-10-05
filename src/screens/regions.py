import pygame

from enum import Enum, auto

from src.screens.base_screen import BaseScreen

from src.ui.region.region_details_view import RegionDetailsView
from src.ui.region.region_form import RegionForm

from src.ui.location.location_form import LocationForm

from src.ui.dialogs.confirm_dialog import ConfirmDialog
from src.ui.dialogs.message_dialog import MessageDialog

class RegionViewMode(Enum):
    DETAILS = auto()
    REGION_FORM = auto()
    LOCATION_FORM = auto()

class RegionScreen(BaseScreen):
    def __init__(
        self,
        app,
        region
    ):
        super().__init__(
            app,
            "world"
        )
        
        self.region = region
        self.locations = []
        
        self.details_view = RegionDetailsView()
        
        self.region_form = RegionForm()
        self.location_form = LocationForm()
                
        self.view_mode = RegionViewMode.DETAILS

        self.refresh_locations()
        
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
                
            if action == "confirm":
                self.confirm_delete_region()
                return
                
            return
        
        super().handle_event(
            event
        )

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == RegionViewMode.REGION_FORM
            ):
                self.cancel_region_form()
                return
            
            if (
                self.view_mode
                == RegionViewMode.LOCATION_FORM
            ):
                self.cancel_location_form()
                return
            
            self.return_to_world()
            return
        
        if (
            self.view_mode
            == RegionViewMode.REGION_FORM
        ):
            self.handle_region_form_events(
                event
            )
            return
        
        if (
            self.view_mode
            == RegionViewMode.LOCATION_FORM
        ):
            self.handle_location_form_events(
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
        action, location = (
            self.details_view.handle_event(
                event
            )
        )
        
        if action == "edit_region":
            self.region_form.prepare_edit(
                self.region
            )
            
            self.view_mode = (
                RegionViewMode.REGION_FORM
            )
            
            return
        
        if action == "delete_region":
            self.request_delete_region()
            return
        
        if action == "back":
            self.return_to_world()
            return
        
        if action == "new_location":
            self.location_form.prepare_create()
            
            self.view_mode = (
                RegionViewMode.LOCATION_FORM
            )
            
            return
        
        if (
            action == "select_location"
            and location is not None
        ):
            self.select_location(
                location
            )
    
    def handle_region_form_events(
        self,
        event
    ):
        action = (
            self.region_form.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.cancel_region_form()
            return
        
        if action == "submit":
            self.update_region()
            return
    
    def handle_location_form_events(
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
            self.create_location()
            return
    
    def cancel_location_form(self):
        self.location_form.clear()
        
        self.view_mode = (
            RegionViewMode.DETAILS
        )

    def create_location(self):
        if self.region.id is None:
            return
        
        location = (
            self.location_form.build_location(
                region_id=self.region.id
            )
        )
        
        if location is None:
            return
        
        self.app.location_repository.add(
            location
        )
        
        self.refresh_locations()
        
        self.location_form.clear()
        
        self.view_mode = (
            RegionViewMode.DETAILS
        )
        
    def refresh_locations(self):
        if self.region.id is None:
            self.locations = []
            return

        self.locations = (
            self.app
            .location_repository
            .get_all_by_region(
                self.region.id
            )
        )

    def return_to_world(self):
        self.app.open_world()

    def update(self):
        pass

    def render(
        self,
        screen
    ):
        super().render(
            screen
        )
        
        if (
            self.view_mode
            == RegionViewMode.REGION_FORM
        ):
            self.region_form.render(
                screen
            )

        elif (
            self.view_mode
            == RegionViewMode.LOCATION_FORM
        ):
            self.location_form.render(
                screen
            )
            
        else:
            self.details_view.render(
                screen,
                self.region,
                self.locations
            )
            
        self.message_dialog.render(
            screen
        )
        
        self.confirm_dialog.render(
            screen
        )
            
    def select_location(
        self,
        location
    ):
        self.app.open_location(
            self.region,
            location
        )

    def cancel_region_form(self):
        self.region_form.clear()
        
        self.view_mode = (
            RegionViewMode.DETAILS
        )
        
    def update_region(self):
        updated_region = (
            self.region_form.build_region(
                self.region.world_id
            )
        )
        
        if updated_region is None:
            return
        
        self.app.region_repository.update(
            updated_region
        )
        
        refreshed_region = (
            self.app
            .region_repository
            .get_by_id(
                updated_region.id
            )
        )
        
        if refreshed_region is not None:
            self.region = refreshed_region
        else:
            self.region = updated_region
            
        self.region_form.clear()
        
        self.view_mode = (
            RegionViewMode.DETAILS
        )
        
    def request_delete_region(self):
        if self.region.id is None:
            return
        
        locations = (
            self.app
            .location_repository
            .get_all_by_region(
                self.region.id
            )
        )
        
        if locations:
            location_count = len(
                locations
            )
            
            locations_label = (
                "local"
                if location_count == 1
                else "locais"
            )
            
            self.message_dialog.set_message(
                "Não é possível excluir",
                (
                    f'"{self.region.name}" possui '
                    f"{location_count} {locations_label}"
                )
            )
            
            self.message_dialog.open()
            return
        
        self.confirm_dialog.open(
            "Excluir região?",
            (
                f'Tem certeza que deseja excluir '
                f'"{self.region.name}"?'
            ),
            "Esta ação não pode ser desfeita.",
            "Excluir"
        )

    def confirm_delete_region(self):
        self.confirm_dialog.close()
        
        try:
            self.app.region_repository.delete(
                self.region
            )
            
        except ValueError as error:
            self.message_dialog.set_message(
                "Não é possível excluir",
                str(error)
            )
            
            self.message_dialog.open()
            return
        
        self.return_to_world()
