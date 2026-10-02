import pygame

from src.screens.base_screen import BaseScreen

from src.ui.location.location_details_view import (
    LocationDetailsView
)


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
            self.return_to_region()
            return
        
        action = (
            self.details_view.handle_event(
                event
            )
        )
        
        if action == "back":
            self.return_to_region()
            return
        
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