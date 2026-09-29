import pygame

class TextArea:
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
            24
        )
        
        self.background_color = (40, 40, 48)
        self.border_color = (80, 80, 95)
        self.active_border_color = (120, 120, 160)
        
        self.text_color = (235, 235, 240)
        self.placeholder_color = (130, 130, 140)
        
        self.padding = 10
        
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
                self.text += "\n"
            
            elif event.key == pygame.K_TAB:
                pass
            
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

        lines = self.wrap_text(display_text)

        y = self.rect.y + self.padding

        for line in lines:
            text_surface = self.font.render(
                line,
                True,
                color
            )

            screen.blit(
                text_surface,
                (
                    self.rect.x + self.padding,
                    y
                )
            )

            y += self.font.get_linesize()

            if y > self.rect.bottom - self.padding:
                break

    def wrap_text(self, text):
        max_width = (
            self.rect.width
            - self.padding * 2
        )

        lines = []

        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            words = paragraph.split(" ")

            current_line = ""

            for word in words:

                test_line = current_line

                if test_line:
                    test_line += " "

                test_line += word

                width, _ = self.font.size(
                    test_line
                )

                if width <= max_width:
                    current_line = test_line

                else:
                    if current_line:
                        lines.append(
                            current_line
                        )

                    current_line = word

            lines.append(current_line)

        return lines