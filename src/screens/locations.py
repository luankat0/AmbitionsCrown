import pygame

from enum import Enum, auto

from src.screens.base_screen import BaseScreen

from src.ui.location.location_details_view import (
    LocationDetailsView
)
from src.ui.location.location_form import (
    LocationForm
)

class LocationViewMode(Enum):
    DETAILS = auto()
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
        
        self.child_form = LocationForm()
        
        self.view_mode = (
            LocationViewMode.DETAILS
        )
        
        self.refresh_children()
        
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
                == LocationViewMode.CHILD_FORM
            ):
                self.cancel_child_form()
                return
            
            self.navigate_back()
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
        
        if action == "new_child":
            self.child_form.prepare_create()
            
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
            self.child_form.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.cancel_child_form()
            return
        
        if action == "submit":
            self.create_child()
            return
        
    def cancel_child_form(self):
        self.child_form.clear()
        
        self.view_mode = (
            LocationViewMode.DETAILS
        )
        
    def create_child(self):
        if (
            self.region.id is None
            or self.location.id is None
        ):
            return
        
        child = (
            self.child_form.build_location(
                region_id=self.region.id,
                parent_location_id=(
                    self.location.id
                )
            )
        )
        
        if child is None:
            return
        
        self.app.location_repository.add(
            child
        )
        
        self.refresh_children()
        
        self.child_form.clear()
        
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
        
        if (
            self.view_mode
            == LocationViewMode.CHILD_FORM
        ):
            self.child_form.render(
                screen
            )
        
        else:
            self.details_view.render(
                screen,
                self.location,
                self.children
            )
        
    def refresh_children(self):
        if self.location.id is None:
            self.children = []
            return
        
        self.children = (
            self.app
            .location_repository
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
            .location_repository
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
