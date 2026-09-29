import pygame

class DashboardScreen:
    def __init__(self):
        self.background_color = (30, 30, 35)
        
        self.menu_font = pygame.font.Font(
            None,
            28
        )

        self.menu_items = [
            "Dashboard",
            "Campanha",
            "Jogadores",
            "NPCs",
            "Bestiário",
            "Mundo",
            "Missões",
        ]

        self.title_font = pygame.font.Font(
            None,
            48
        )

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.background_color)

        pygame.draw.rect(
            screen,
            (22, 22, 28),
            (0, 0, 240, screen.get_height())
        )

        title = self.title_font.render(
            "Ambitions Crown",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title,
            (50, 40)
        )

        y = 120

        for item in self.menu_items:
            text = self.menu_font.render(
                item,
                True,
                (200, 200, 205)
            )

            screen.blit(
                text,
                (30, y)
            )

            y += 50