import pygame

from src.models.npc import NPC

from src.ui.button import Button
from src.ui.text_area import TextArea
from src.ui.text_input import TextInput

class NPCForm:
    def __init__(self):
        self.mode = "create"
        
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            26
        )
        
        # -------------------------
        # Informações Básicas
        # -------------------------
        
        self.name_input = TextInput(
            420,
            150,
            280,
            42,
            "Nome do NPC"
        )
        
        self.race_input = TextInput(
            420,
            220,
            280,
            42,
            "Raça"
        )
        
        self.role_input = TextInput(
            420,
            290,
            280,
            42,
            "Profissão ou Classe"
        )
        
        self.region_input = TextInput(
            420,
            360,
            280,
            42,
            "Região"
        )
        
        # -------------------------
        # Caracterização
        # -------------------------
        
        self.description_input = TextArea(
            800,
            150,
            380,
            110,
            "Aparência, histórico ou descrição geral..."
        )
        
        self.personality_input = TextArea(
            800,
            300,
            380,
            110,
            "Personalidade, comportamento, manias..."
        )
        
        self.notes_input = TextArea(
            800,
            450,
            380,
            110,
            "Anotações privadas do Mestre..."
        )
        
        self.fields = [
            self.name_input,
            self.race_input,
            self.role_input,
            self.region_input,
            self.description_input,
            self.personality_input,
            self.notes_input
        ]
        
        # -------------------------
        # Botões
        # -------------------------
        
        self.cancel_button = Button(
            800,
            590,
            140,
            45,
            "Cancelar"
        )
                
        self.submit_button = Button(
            960,
            590,
            160,
            45,
            "Criar NPC"
        )
        
        self.validation_message = ""
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                shift_pressed = bool(
                    event.mod & pygame.KMOD_SHIFT
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
                    event.mod & pygame.KMOD_SHIFT
                )
                
                active_index = (
                    self._get_active_index()
                )
                
                active_field = None
                
                if active_index is not None:
                    active_field = (
                        self.fields[active_index]
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
        
        self.name_input.handle_event(event)
        if self.name_input.text.strip():
            self.name_input.error = False
            self.validation_message = ""
            
        self.race_input.handle_event(event)
        self.role_input.handle_event(event)
        self.region_input.handle_event(event)

        self.description_input.handle_event(event)
        self.personality_input.handle_event(event)
        self.notes_input.handle_event(event)

        if self.cancel_button.handle_event(event):
            return "cancel"

        if self.submit_button.handle_event(event):
            return "submit"

        return None
    
    def prepare_create(self):
        self.mode = "create"
            
        self.clear()
            
        self.submit_button.text = "Criar NPC"
        
        self._set_focus(0)
    
    def load_npc(self, npc):
        self.mode = "edit"

        self.name_input.text = npc.name
        self.race_input.text = npc.race
        self.role_input.text = npc.role
        self.region_input.text = npc.region

        self.description_input.text = npc.description
        self.personality_input.text = npc.personality
        self.notes_input.text = npc.notes

        self.submit_button.text = "Salvar"
                
        for field in [
            self.name_input,
            self.race_input,
            self.role_input,
            self.region_input,
        ]:
            field.cursor_index = len(
                field.text
            )
            
            field.scroll_x = 0
            
        for field in [
            self.description_input,
            self.personality_input,
            self.notes_input
        ]:
            field.cursor_index = len(
                field.text
            )
            
            field.scroll_line = 0
            
            
        self._set_focus(0)
        
    def build_npc(self):
        if not self.validate():
            return None
        
        name = self.name_input.text.strip()

        return NPC(
            name=name,
            race=self.race_input.text.strip(),
            role=self.role_input.text.strip(),
            region=self.region_input.text.strip(),
            description=self.description_input.text.strip(),
            personality=self.personality_input.text.strip(),
            notes=self.notes_input.text.strip()
        )
        
    def clear(self):
        self.name_input.text = ""
        self.race_input.text = ""
        self.role_input.text = ""
        self.region_input.text = ""

        self.description_input.text = ""
        self.personality_input.text = ""
        self.notes_input.text = ""
        
        for field in self.fields:
            field.active = False
        
        for field in [
            self.name_input,
            self.race_input,
            self.role_input,
            self.region_input,
        ]:
            field.cursor_index = 0
            field.scroll_x = 0
            
        for field in [
            self.description_input,
            self.personality_input,
            self.notes_input,
        ]:
            field.cursor_index = len(
                field.text
            )
            
            field.scroll_line = 0
            
        self.name_input.error = False
        self.validation_message = ""
        
    def render(self, screen):
        # -------------------------
        # Título
        # -------------------------
        if self.mode == "edit":
            title_text = "Editar NPC"
        else:
            title_text = "Criar NPC"
            
        title = self.title_font.render(
            title_text,
            True,
            (240, 240, 240)
        )
        
        screen.blit(
            title,
            (280, 40)
        )
        
        # -------------------------
        # Títulos das seções
        # -------------------------
        
        basic_title = self.info_font.render(
            "Informações básicas",
            True,
            (180, 180, 200)
        )
        
        screen.blit(
            basic_title,
            (300, 105)
        )

        characterization_title = self.info_font.render(
            "Caracterização",
            True,
            (180, 180, 200)
        )

        screen.blit(
            characterization_title,
            (800, 105)
        )

        # -------------------------
        # Labels básicos
        # -------------------------

        basic_labels = [
            ("Nome", 150),
            ("Raça", 220),
            ("Função", 290),
            ("Região", 360),
        ]

        for label, y in basic_labels:
            label_surface = self.info_font.render(
                label,
                True,
                (200, 200, 210)
            )

            screen.blit(
                label_surface,
                (300, y + 10)
            )

        # -------------------------
        # Labels dos TextAreas
        # -------------------------

        description_label = self.info_font.render(
            "Descrição",
            True,
            (200, 200, 210)
        )

        personality_label = self.info_font.render(
            "Personalidade",
            True,
            (200, 200, 210)
        )

        notes_label = self.info_font.render(
            "Observações",
            True,
            (200, 200, 210)
        )

        screen.blit(
            description_label,
            (800, 125)
        )

        screen.blit(
            personality_label,
            (800, 275)
        )

        screen.blit(
            notes_label,
            (800, 425)
        )

        # -------------------------
        # Inputs básicos
        # -------------------------

        self.name_input.render(screen)
        if self.validation_message:
            error_surface = self.info_font.render(
                self.validation_message,
                True,
                (200, 90, 100)
            )
            
            screen.blit(
                error_surface,
                (420, 195)
            )
        self.race_input.render(screen)
        self.role_input.render(screen)
        self.region_input.render(screen)

        # -------------------------
        # TextAreas
        # -------------------------

        self.description_input.render(screen)
        self.personality_input.render(screen)
        self.notes_input.render(screen)

        # -------------------------
        # Botões
        # -------------------------

        self.cancel_button.render(screen)
        self.submit_button.render(screen)
    
    def _set_focus(self, index):
        for field in self.fields:
            field.active = False
        
        active_field = self.fields[index]
        
        active_field.active = True
        
        if isinstance(
            active_field,
            TextArea
        ):
            active_field.ensure_cursor_visible()
    
    def _get_active_index(self):
        for index, field in enumerate(self.fields):
            if field.active:
                return index
            
        return None

    def _move_focus(self, direction):
        current_index = self._get_active_index()
        
        if current_index is None:
            if direction > 0:
                next_index = 0
            else:
                next_index = len(self.fields) - 1
        
        else:
            next_index = (
                current_index + direction
            ) % len(self.fields)
            
        self._set_focus(next_index)
        
    def validate(self):
        self.name_input.error = False
        self.validation_message = ""
        
        if not self.name_input.text.strip():
            self.name_input.error = True
            
            self.validation_message = (
                "O nome do NPC é obrigatório."
            )
            
            return False
        
        return True
    
