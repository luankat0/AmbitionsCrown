import pygame

from src.domain.world.models.location import (
    Location,
    LocationType
)

from src.domain.campaign.models.campaign_location import (
    CampaignLocation,
)

from src.ui.base_form import BaseForm
from src.ui.button import Button
from src.ui.text_area import TextArea
from src.ui.text_input import TextInput

from src.ui.location.location_labels import (
    get_location_type_label
)


class LocationForm(BaseForm):
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
            "Nome do local"
        )

        self.type_button = Button(
            420,
            220,
            220,
            45,
            "Outro"
        )

        self.description_input = TextArea(
            760,
            150,
            420,
            160,
            "Descrição do local..."
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
            "Criar Local"
        )

        self.fields = [
            self.name_input,
            self.description_input,
            self.notes_input,
        ]
        
        self.mode = "create"
        self.editing_location_id = None

        self.location_types = list(
            LocationType
        )

        self.location_type_index = (
            self.location_types.index(
                LocationType.OTHER
            )
        )
    
    @property
    def selected_location_type(self):
        return self.location_types[
            self.location_type_index
        ]
        
    def _update_type_button(self):
        self.type_button.text = (
            get_location_type_label(
                self.selected_location_type
            )
        )
        
    def _next_location_type(self):
        self.location_type_index = (
            self.location_type_index + 1
        ) % len(self.location_types)
        
        self._update_type_button()
        
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
            self._next_location_type()
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
                "O nome do local é obrigatório."
            )
            
            return False
        
        return True
    
    def build_location(
        self,
        region_id: int,
        parent_location_id: int | None = None
    ):
        if not self.validate():
            return None
        
        return Location(
            id=self.editing_location_id,
            region_id=region_id,
            parent_location_id=(
                parent_location_id
            ),
            name=self.name_input.text.strip(),
            location_type=(
                self.selected_location_type
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
            )
        )
    
    def build_campaign_location(
        self,
        campaign_id,
        region_id,
        parent_location_id=None
    ):
        return CampaignLocation(
            campaign_id=campaign_id,
            region_id=region_id,
            parent_location_id=parent_location_id,
            name=self.name_input.text.strip(),
            location_type=self.selected_location_type,
            description=self.description_input.text.strip(),
            notes=self.notes_input.text.strip(),
        )
     
    def prepare_create(self):
        super().prepare_create()
        
        self.mode = "create"
        self.editing_location_id = None
        
        self.location_type_index = (
            self.location_types.index(
                LocationType.OTHER
            )
        )
        
        self._update_type_button()
        
        self.submit_button.text = (
            "Criar Local"
        )
        
    def render(
    self,
    screen
    ):
        title_surface = (
            self.title_font.render(
                "Novo Local",
                True,
                (240, 240, 245)
            )
        )

        screen.blit(
            title_surface,
            (300, 50)
        )

        name_label = (
            self.info_font.render(
                "Nome",
                True,
                (200, 200, 210)
            )
        )

        type_label = (
            self.info_font.render(
                "Tipo",
                True,
                (200, 200, 210)
            )
        )

        description_label = (
            self.info_font.render(
                "Descrição",
                True,
                (200, 200, 210)
            )
        )

        notes_label = (
            self.info_font.render(
                "Anotações",
                True,
                (200, 200, 210)
            )
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
                (420, 200)
            )

        self.cancel_button.render(
            screen
        )

        self.submit_button.render(
            screen
        )
        
    def prepare_edit(
        self,
        location
    ):
        self.clear()
        
        self.mode = "edit"
        self.editing_location_id = (
            location.id
        )
        
        self.name_input.text = (
            location.name
        )
        
        self.name_input.cursor_index = len(
            location.name
        )

        self.description_input.text = (
            location.description
        )
        
        self.description_input.cursor_index = len(
            location.description
        )
        
        self.notes_input.text = (
            location.notes
        )
        
        self.notes_input.cursor_index = len(
            location.notes
        )
        
        self.location_types_index = (
            self.location_types.index(
                location.location_type
            )
        )
        
        self._update_type_button()
        
        self.submit_button.text = "Salvar"
        
        self._set_focus(0)
    