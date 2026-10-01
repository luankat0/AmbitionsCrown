import pygame

from src.models.world import World

from src.ui.button import Button
from src.ui.text_area import TextArea
from src.ui.text_input import TextInput
from src.ui.base_form import BaseForm

class WorldForm(BaseForm):
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
            420,
            150,
            420,
            45,
            "Nome do mundo"
        )
        
        self.description_input = TextArea(
            420,
            260,
            600,
            130,
            "Descrição geral do mundo..."
        )
        
        self.notes_input = TextArea(
            420,
            460,
            600,
            130,
            "Anotações privadas do Mestre..."
        )
        
        self.cancel_button = Button(
            720,
            630,
            140,
            45,
            "Cancelar"
        )
        
        self.submit_button = Button(
            880,
            630,
            160,
            45,
            "Criar Mundo"
        )
        
        self.fields = [
            self.name_input,
            self.description_input,
            self.notes_input
        ]
               
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                shift_pressed = bool(
                    event.mod
                    & pygame.KMOD_SHIFT
                )
                
                if shift_pressed:
                    self._move_focus(-1)
                else:
                    self._move_focus(1)
                    
                return None
            
            if event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            ):
                shift_pressed = bool(
                    event.mod
                    & pygame.KMOD_SHIFT
                )
                
                active_index = (
                    self._get_active_index()
                )
                
                active_field = None
                
                if active_index is not None:
                    active_field = (
                        self.fields[
                            active_index
                        ]
                    )
                
                if (
                    shift_pressed
                    and isinstance(
                        active_field,
                        TextArea
                    )
                ):
                    pass
                
                else:
                    return "submit"
                
        self.name_input.handle_event(
            event
        )
        
        self.description_input.handle_event(
            event
        )
        
        self.notes_input.handle_event(
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
    
    def validate(self):
        self.name_input.error = False
        self.validation_message = ""
        
        if not self.name_input.text.strip():
            self.name_input.error = True
            
            self.validation_message = (
                "O nome do mundo é obrigatório."
            )
            
            return False
        
        return True
    
    def build_world(self):
        if not self.validate():
            return None
        
        return World(
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
              
    def render(self, screen):
        title = self.title_font.render(
            "Novo Mundo",
            True,
            (240, 240, 245)
        )

        screen.blit(
            title,
            (300, 50)
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
            (300, 160)
        )

        screen.blit(
            description_label,
            (300, 270)
        )

        screen.blit(
            notes_label,
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
                (420, 205)
            )

        self.cancel_button.render(
            screen
        )

        self.submit_button.render(
            screen
        )

