import pygame

class TextInput:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        placeholder=""
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = ""
        self.placeholder = placeholder

        self.active = False

        self.font = pygame.font.Font(
            None,
            26
        )

        self.background_color = (40, 40, 48)
        self.border_color = (80, 80, 95)
        self.active_border_color = (120, 120, 160)

        self.text_color = (235, 235, 240)
        self.placeholder_color = (130, 130, 140)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.active = self.rect.collidepoint(
                    event.pos
                )

        if event.type == pygame.KEYDOWN and self.active:

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                self.active = False

            else:
                self.text += event.unicode

    def render(self, screen):
        pygame.draw.rect(
            screen,
            self.background_color,
            self.rect,
            border_radius=5
        )

        if self.active:
            border_color = self.active_border_color
        else:
            border_color = self.border_color

        pygame.draw.rect(
            screen,
            border_color,
            self.rect,
            width=2,
            border_radius=5
            )

        if self.text:
            display_text = self.text
            color = self.text_color
        else:
            display_text = self.placeholder
            color = self.placeholder_color

        text_surface = self.font.render(
            display_text,
            True,
            color
        )

        screen.blit(
            text_surface,
            (
                self.rect.x + 10,
                self.rect.centery
                - text_surface.get_height() // 2
            )
        )