import pygame

class Button:
    def __init__(
        self, 
        x,
        y,
        width,
        height,
        text
    ):
        self.rect = pygame.Rect(
            x,
            y, 
            width,
            height
        )

        self.text = text

        self.background_color = (65, 65, 85)
        self.hover_color = (80, 80, 105)
        self.text_color = (240, 240, 245)

        self.font = pygame.font.Font(
            None,
            26
        )

        self.is_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(
                event.pos
            )

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    return True

        return False

    def render(self, screen):
        if self.is_hovered:
            color = self.hover_color
        else:
            color = self.background_color

        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=6
        )

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )
