import pygame

class BaseDialog:
    def __init__(
        self,
        title,
        width=520,
        height=260
    ):
        self.title = title
        
        self.width = width
        self.height = height
        
        self.visible = False
        
        self.title_font = pygame.font.Font(
            None,
            34
        )
        
        self.text_font = pygame.font.Font(
            None,
            24
        )
        
        self.overlay_color = (
            0,
            0,
            0,
            150
        )
        
        self.background_color = (
            42,
            42,
            52
        )
        
        self.border_color = (
            80,
            80,
            95
        )
        
        self.title_color = (
            235,
            235,
            240
        )
        
    def open(self):
        self.visible = True
        
    def close(self):
        self.visible = False
        
    def handle_base_event(
        self,
        event
    ):
        if not self.visible:
            return False
        
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            self.close()
            return True
        
        return False
    
    def get_rect(
        self,
        screen
    ):
        screen_rect = screen.get_rect()
        
        return pygame.Rect(
            screen_rect.centerx
            - self.width // 2,
            
            screen_rect.centery
            - self.height // 2,
            
            self.width,
            self.height
        )
        
    def render_base(
        self,
        screen
    ):
        if not self.visible:
            return None
        
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )
        
        overlay.fill(
            self.overlay_color
        )
        
        screen.blit(
            overlay,
            (0, 0)
        )
        
        dialog_rect = self.get_rect(
            screen
        )
        
        pygame.draw.rect(
            screen,
            self.background_color,
            dialog_rect,
            border_radius=10
        )
        
        pygame.draw.rect(
            screen,
            self.border_color,
            dialog_rect,
            width=2,
            border_radius=10
        )
        
        title_surface = (
            self.title_font.render(
                self.title,
                True,
                self.title_color
            )
        )
        
        screen.blit(
            title_surface,
            (
                dialog_rect.x + 30,
                dialog_rect.y + 25
            )
        )
        
        return dialog_rect