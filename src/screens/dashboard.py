import pygame

class DashboardScreen:
    def __init__(self, app):
        self.app = app
        
        self.background_color = (30, 30, 35)

        self.menu_font = pygame.font.Font(
            None,
            28
        )

        self.title_font = pygame.font.Font(
            None,
            48
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

        self.menu_rects = {}

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_position = event.pos

                npc_rect = self.menu_rects.get("NPCs")

                if npc_rect and npc_rect.collidepoint(mouse_position):
                    self.app.change_screen("npcs")

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

        self.menu_rects.clear()

        for item in self.menu_items:
            text = self.menu_font.render(
                item,
                True,
                (200, 200, 205)
            )

            rect = text.get_rect(
                topleft=(30, y)
            )

            self.menu_rects[item] = rect

            screen.blit(
                text,
                rect
            )

            y += 50