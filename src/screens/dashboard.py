import pygame

from src.screens.base_screen import BaseScreen

class DashboardScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(
            app,
            "dashboard"
        )

        self.title_font = pygame.font.Font(
            None, 
            48
        )

    def render(self, screen):
        super().render(screen)

        title = self.title_font.render(
            "Ambitions Crown",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title,
            (280, 40)
        )