import pygame

from enum import Enum, auto

from src.screens.base_screen import BaseScreen

from src.ui.region.region_details_view import RegionDetailsView
from src.ui.location.location_form import LocationForm

class RegionViewMode(Enum):
    DETAILS = auto()
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
        
        self.location_form = LocationForm()
        self.details_view = RegionDetailsView()
                
        self.view_mode = RegionViewMode.DETAILS

        self.refresh_locations()

    def handle_event(
        self,
        event
    ):
        super().handle_event(
            event
        )

        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
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
        self.app.change_screen(
            "world"
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

        if (
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
            
    def select_location(
        self,
        location
    ):
        self.app.open_location(
            self.region,
            location
        )