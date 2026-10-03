import pygame

from src.ui.button import Button
from src.ui.dialogs.base_dialog import BaseDialog

class MessageDialog(BaseDialog):
    def __init__(
        self,
        title,
        message,
        width=520,
        height=260
    ):
        super().__init__(
            title,
            width,
            height
        )
        
        self.message = message
        
        self.ok_button = Button(
            0,
            0,
            120,
            42,
            "OK"
        )
        
    def set_message(
        self,
        title,
        message
    ):
        self.title = title
        self.message = message
            
            
    def handle_event(
        self,
        event
    ):
        if not self.visible:
            return None
            
        if self.handle_base_event(
            event
        ):
            return "close"
            
        if self.ok_button.handle_event(
            event
        ):
            self.close()
            return "close"
            
        return None

    def render(
        self,
        screen
    ):
        dialog_rect = self.render_base(
            screen
        )
        
        if dialog_rect is None:
            return
        
        message_surface = (
            self.text_font.render(
                self.message,
                True,
                (200, 200, 210)
            )
        )
        
        screen.blit(
            message_surface,
            (
                dialog_rect.x + 30,
                dialog_rect.y + 90
            )
        )
        
        self.ok_button.rect.x = (
            dialog_rect.right
            - self.ok_button.rect.width
            - 30
        )
        
        self.ok_button.rect.y = (
            dialog_rect.bottom
            - self.ok_button.rect.height
            - 25
        )
        
        self.ok_button.render(
            screen
        )