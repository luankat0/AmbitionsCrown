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
        
        self.campaign_font = pygame.font.Font(
            None,
            22
        )
        
        self.campaign_name_font = pygame.font.Font(
            None,
            24
        )
        
        self.back_campaign_rect = pygame.Rect(
            20,
            20,
            self.width - 40,
            32
        )

        self.menu_items = [
            ("Dashboard", "dashboard"),
            ("Mundo", "world"),
            ("Facções", "factions"),
            ("NPCs", "npcs"),
        ]

        self.menu_rects = {}

        self.create_menu_rects()

    def create_menu_rects(self):
        y = 150

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
        if (
            event.type == pygame.MOUSEBUTTONDOWN 
            and event.button == 1
        ):
            if (
                self.app.current_campaign
                is not None
                and self.back_campaign_rect.collidepoint(
                    event.pos
                )
            ):
                self.app.return_to_campaigns()
                return
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
        
        campaign = self.app.current_campaign
        
        if campaign is not None:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.back_campaign_rect.collidepoint(
                mouse_pos
            ):
                pygame.draw.rect(
                    screen,
                    self.active_color,
                    self.back_campaign_rect,
                    border_radius=5
                )
                
            back_surface = (
                self.campaign_font.render(
                    "← Campanhas",
                    True,
                    self.text_color
                )
            )
            
            back_rect = back_surface.get_rect(
                midleft=(
                    self.back_campaign_rect.x + 5,
                    self.back_campaign_rect.centery
                )
            )
            
            screen.blit(
                back_surface,
                back_rect
            )
            
            campaign_surface = (
                self.campaign_name_font.render(
                    campaign.name,
                    True,
                    (235, 235, 240)
                )
            )
            
            screen.blit(
                campaign_surface,
                (25, 70)
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
