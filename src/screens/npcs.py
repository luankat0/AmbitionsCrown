import pygame

from src.screens.base_screen import BaseScreen

class NPCScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(
            app,
            "npcs"
        )

        self.title_font = pygame.font.Font(
            None,
            48
        )

    def handle_event(self, event):
        super().handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_screen("dashboard")

    def render(self, screen):
        super().render(screen)

        title = self.title_font.render(
            "NPCs",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title,
            (280, 40)
        )