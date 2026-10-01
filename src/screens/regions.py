import pygame

from src.screens.base_screen import BaseScreen
from src.ui.region.region_details_view import RegionDetailsView


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

        self.details_view = (
            RegionDetailsView()
        )

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
            self.return_to_world()
            return

        action = (
            self.details_view.handle_event(
                event
            )
        )

        if action == "back":
            self.return_to_world()
            return

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

        self.details_view.render(
            screen,
            self.region,
            self.locations
        )