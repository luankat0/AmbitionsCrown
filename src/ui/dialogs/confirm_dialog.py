import pygame

from src.ui.button import Button

from src.ui.dialogs.base_dialog import BaseDialog

class ConfirmDialog(BaseDialog):
    def __init__(self):
        super().__init__(
            "",
            width=480,
            height=240
        )
                
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
        
        self.background_color = (
            36,
            36,
            44
        )
        
        self.border_color = (
            90,
            90,
            105
        )
        
        self.title_color = (
            240,
            240,
            240
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
    
    def render(
        self, 
        screen
    ):
        modal_rect = self.render_base(
            screen
        )
        
        if modal_rect is None:
            return
        
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
            
        self.cancel_button.rect.x = (
            modal_rect.x + 80
        )
        
        self.cancel_button.rect.y = (
            modal_rect.bottom - 90
        )
        
        self.confirm_button.rect.x = (
            modal_rect.x + 240
        )
        
        self.confirm_button.rect.y = (
            modal_rect.bottom - 90
        )
        
        self.cancel_button.render(
            screen
        )
        self.confirm_button.render(
            screen
        )
