import pygame

class NPCScreen:
    def __init__(self, app):
        self.app = app

        self.background_color = (30, 30, 35)

        self.title_font = pygame.font.Font(
            None,
            48
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_screen("dashboard")

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.background_color)

        title = self.title_font.render(
            "NPCs",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title,
            (280, 40)
        )