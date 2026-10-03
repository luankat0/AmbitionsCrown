import pygame

from src.ui.button import Button

from src.ui.dialogs.base_dialog import BaseDialog

class ConfirmDialog(BaseDialog):
    def __init__(self):
        super().__init__("")
                
        self.message: str = ""
        self.warning: str = ""
        
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            26
        )
        
        self.cancel_button = Button(
            500,
            400,
            140,
            45,
            "Cancelar"
        )
        
        self.confirm_button = Button(
            660,
            400,
            140,
            45,
            "Confirmar"
        )
        
    def open(
        self,
        title,
        message,
        warning="",
        confirm_text="Confirmar"
    ):
        self.title = title
        self.message = message
        self.warning = warning
        
        self.confirm_button.text = confirm_text
        
        self.visible = True
        
    def handle_event(self, event):
        if  not self.visible:
            return None
        
        if self.handle_base_event(
            event
        ):
            return "cancel"
            
        if self.cancel_button.handle_event(event):
            return "cancel"
        
        if self.confirm_button.handle_event(event):
            return "confirm"
        
        return None
    
    def render(self, screen):
        if not self.visible:
            return
        
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )
        
        overlay.fill(
            (0, 0, 0, 150)
        )
        
        screen.blit(
            overlay, 
            (0, 0)
        )
        
        modal_rect = pygame.Rect(
            420,
            250,
            480,
            240
        )
        
        pygame.draw.rect(
            screen,
            (36, 36, 44),
            modal_rect,
            border_radius=10
        )
        
        pygame.draw.rect(
            screen,
            (90, 90, 105),
            modal_rect,
            width=2,
            border_radius=10
        )
        
        title_surface = self.title_font.render(
            self.title,
            True,
            (240, 240, 240)
        )
        
        screen.blit(
            title_surface,
            (
                modal_rect.x + 30,
                modal_rect.y + 25
            )
        )
        
        message_surface = self.info_font.render(
            self.message,
            True,
            (210, 210, 220)
        )
        
        screen.blit(
            message_surface,
            (
                modal_rect.x + 30,
                modal_rect.y + 90
            )
        )
        
        if self.warning:
            warning_surface = self.info_font.render(
                self.warning,
                True,
                (170, 170, 180)
            )
            
            screen.blit(
                warning_surface,
                (
                    modal_rect.x + 30,
                    modal_rect.y + 125
                )
            )
        self.cancel_button.render(screen)
        self.confirm_button.render(screen)