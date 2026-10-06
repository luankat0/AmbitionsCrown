import pygame

from src.domain.campaign.models.campaign import Campaign

from src.ui.button import Button
from src.ui.text_area import TextArea
from src.ui.text_input import TextInput
from src.ui.base_form import BaseForm

class CampaignForm(BaseForm):
    def __init__(self):
        super().__init__()
        
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            26
        )
        
        self.name_input = TextInput(
            380,
            160,
            420,
            45,
            "Nome da campanha"
        )
        
        self.description_input = TextArea(
            380,
            260,
            600,
            130,
            "Descrição da campanha..."
        )
        
        self.notes_input = TextArea(
            380,
            460,
            600,
            130,
            "Anotações do Mestre..."
        )
        
        self.cancel_button = Button(
            680,
            630,
            140,
            45,
            "Cancelar"
        )
        
        self.submit_button = Button(
            840,
            630,
            180,
            45,
            "Criar Campanha"
        )
        
        self.fields = [
            self.name_input,
            self.description_input,
            self.notes_input
        ]
        
    def handle_event(self, event):
        handled, action = (
            self.handle_navigation_event(
                event
            )
        )
        
        if handled:
            return action
        
        self.handle_fields_event(
            event
        )
        
        if self.name_input.text.strip():
            self.name_input.error = False
            self.validation_message = ""
        
        if self.cancel_button.handle_event(
            event
        ):
            return "cancel"
        
        if self.submit_button.handle_event(
            event
        ):
            return "submit"
        
        return None
    
    def render(self, screen):
        title = self.title_font.render(
            "Nova Campanha",
            True,
            (240, 240, 245)
        )
        
        screen.blit(
            title,
            (300, 60)
        )
        
        name_label = self.info_font.render(
            "Nome",
            True,
            (200, 200, 210)
        )
        
        description_label = (
            self.info_font.render(
                "Descrição",
                True,
                (200, 200, 210)
            )
        )
        
        notes_label = self.info_font.render(
            "Anotações",
            True,
            (200, 200, 210)
        )
        
        screen.blit(
            name_label,
            (300, 170)
        )
        
        screen.blit(
            description_label,
            (300, 470)
        )
        
        self.name_input.render(
            screen
        )
        
        self.description_input.render(
            screen
        )
        
        self.notes_input.render(
            screen
        )
        
        if self.validation_message:
            error_surface = (
                self.info_font.render(
                    self.validation_message,
                    True,
                    (200, 90, 100)
                )
            )
            
            screen.blit(
                error_surface,
                (380, 215)
            )
        
        self.cancel_button.render(
            screen
        )
        
        self.submit_button.render(
            screen
        )
            
    def validate(self):
        self.name_input.error = False
        self.validation_message = ""
        
        if not self.name_input.text.strip():
            self.name_input.error = True
            
            self.validation_message = (
                "O nome da campanha é obrigatório."
            )
            
            return False
        
        return True
    
    def build_campaign(self):
        if not self.validate():
            return None
        
        return Campaign(
            name=self.name_input.text.strip(),
            description=(
                self.description_input
                .text
                .strip()
            ),
            notes=(
                self.notes_input
                .text
                .strip()
            )
        )
                
