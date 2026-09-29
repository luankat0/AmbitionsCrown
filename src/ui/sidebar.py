import pygame

class Sidebar:
    def __init__(self, app, active_screen):
        self.app = app
        self.active_screen = active_screen

        self.width = 240

        self.background_color = (22, 22, 28)
        self.text_color = (200, 200, 205)
        self.active_color = (55, 55, 70)

        self.font = pygame.font.Font(
            None,
            28
        )

        self.menu_items = [
            ("Dashboard", "dashboard"),
            ("NPCs", "npcs")
        ]

        self.menu_rects = {}

        self.create_menu_rects()

    def create_menu_rects(self):
        y = 120

        for label, screen_name in self.menu_items:
            rect = pygame.Rect(
                20,
                y,
                self.width - 40,
                40
            )

            self.menu_rects[screen_name] = rect

            y += 50

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                # Percorre as opções de acesso na barra (dashboard, npcs, ...)
                for screen_name, rect in self.menu_rects.items():

                    if rect.collidepoint(event.pos):
                        self.app.change_screen(screen_name)
                        return

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.background_color,
            (0, 0, self.width, screen.get_height())
        )

        for label, screen_name in self.menu_items:
            rect = self.menu_rects[screen_name]

            if screen_name == self.active_screen:
                pygame.draw.rect(
                    screen,
                    self.active_color,
                    rect
                )

            text = self.font.render(
                label,
                True,
                self.text_color
            )

            text_rect = text.get_rect(
                midleft=(rect.x + 10, rect.centery)
            )

            screen.blit(
                text,
                text_rect
            )