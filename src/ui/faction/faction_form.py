import pygame

from src.models.faction import (
    Faction,
    FactionStatus,
    FactionType,
)

from src.ui.base_form import BaseForm
from src.ui.button import Button
from src.ui.text_area import TextArea
from src.ui.text_input import TextInput

from src.ui.faction.faction_labels import (
    get_faction_status_label,
    get_faction_type_label,
)


class FactionForm(BaseForm):
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
            360,
            45,
            "Nome da facção"
        )

        self.type_button = Button(
            420,
            220,
            260,
            45,
            "Outro"
        )

        self.status_button = Button(
            420,
            290,
            220,
            45,
            "Ativa"
        )

        self.description_input = TextArea(
            760,
            150,
            420,
            160,
            "Descrição da facção..."
        )

        self.notes_input = TextArea(
            760,
            380,
            420,
            160,
            "Anotações privadas do Mestre..."
        )

        self.cancel_button = Button(
            820,
            590,
            140,
            45,
            "Cancelar"
        )

        self.submit_button = Button(
            980,
            590,
            160,
            45,
            "Criar Facção"
        )

        self.fields = [
            self.name_input,
            self.description_input,
            self.notes_input,
        ]
        
        self.edit_faction_id = None
        self.title_text = "Nova Facção"

        self.faction_types = list(
            FactionType
        )

        self.faction_type_index = (
            self.faction_types.index(
                FactionType.OTHER
            )
        )

        self.faction_statuses = list(
            FactionStatus
        )

        self.faction_status_index = (
            self.faction_statuses.index(
                FactionStatus.ACTIVE
            )
        )

        self._update_type_button()
        self._update_status_button()

    @property
    def selected_faction_type(self):
        return self.faction_types[
            self.faction_type_index
        ]

    @property
    def selected_faction_status(self):
        return self.faction_statuses[
            self.faction_status_index
        ]

    def _update_type_button(self):
        self.type_button.text = (
            get_faction_type_label(
                self.selected_faction_type
            )
        )

    def _update_status_button(self):
        self.status_button.text = (
            get_faction_status_label(
                self.selected_faction_status
            )
        )

    def _next_faction_type(self):
        self.faction_type_index = (
            self.faction_type_index + 1
        ) % len(
            self.faction_types
        )

        self._update_type_button()

    def _next_faction_status(self):
        self.faction_status_index = (
            self.faction_status_index + 1
        ) % len(
            self.faction_statuses
        )

        self._update_status_button()

    def handle_event(
        self,
        event
    ):
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

        if self.type_button.handle_event(
            event
        ):
            self._next_faction_type()
            return None

        if self.status_button.handle_event(
            event
        ):
            self._next_faction_status()
            return None

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
                "O nome da facção é obrigatório."
            )

            return False

        return True

    def build_faction(
        self,
        world_id
    ):
        if not self.validate():
            return None

        return Faction(
            id=self.editing_faction_id,
            world_id=world_id,
            name=self.name_input.text.strip(),
            faction_type=(
                self.selected_faction_type
            ),
            status=(
                self.selected_faction_status
            ),
            description=(
                self.description_input
                .text
                .strip()
            ),
            notes=(
                self.notes_input
                .text
                .strip()
            ),
        )

    def prepare_create(self):
        super().prepare_create()
        
        self.editing_faction_id = None
        self.title_text = "Nova Facção"

        self.faction_type_index = (
            self.faction_types.index(
                FactionType.OTHER
            )
        )

        self.faction_status_index = (
            self.faction_statuses.index(
                FactionStatus.ACTIVE
            )
        )

        self._update_type_button()
        self._update_status_button()

        self.submit_button.text = (
            "Criar Facção"
        )

    def prepare_edit(
        self,
        faction
    ):
        self.clear()
        
        self.editing_faction_id = faction.id
        self.title_text = "Editar Facção"
        
        self.name_input.text = faction.name
        self.description_input.text = (
            faction.description
        )
        self.notes_input.text = (
            faction.notes
        )
        
        self.name_input.cursor_index = len(
            self.name_input.text
        )
        
        self.description_input.cursor_index = len(
            self.description_input.text
        )
        
        self.notes_input.cursor_index = len(
            self.notes_input.text
        )
        
        self.faction_type_index = (
            self.faction_types.index(
                faction.faction_type
            )
        )
        
        self.faction_status_index = (
            self.faction_statuses.index(
                faction.status
            )
        )
        
        self._update_type_button()
        self._update_status_button()
        
        self.submit_button.text = "Salvar"
        
        self._set_focus(0)

    def render(
        self,
        screen
    ):
        title_surface = (
            self.title_font.render(
                self.title_text,
                True,
                (240, 240, 245)
            )
        )

        screen.blit(
            title_surface,
            (300, 50)
        )

        name_label = self.info_font.render(
            "Nome",
            True,
            (200, 200, 210)
        )

        type_label = self.info_font.render(
            "Tipo",
            True,
            (200, 200, 210)
        )

        status_label = self.info_font.render(
            "Status",
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
            type_label,
            (300, 230)
        )

        screen.blit(
            status_label,
            (300, 300)
        )

        screen.blit(
            description_label,
            (760, 120)
        )

        screen.blit(
            notes_label,
            (760, 350)
        )

        self.name_input.render(
            screen
        )

        self.type_button.render(
            screen
        )

        self.status_button.render(
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
                (420, 350)
            )

        self.cancel_button.render(
            screen
        )

        self.submit_button.render(
            screen
        )
