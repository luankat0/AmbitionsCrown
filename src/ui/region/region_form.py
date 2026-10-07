import pygame

from src.domain.world.models.region import Region, RegionType

from src.domain.campaign.models.campaign_region import (
    CampaignRegion,
)

from src.ui.base_form import BaseForm
from src.ui.button import Button
from src.ui.text_area import TextArea
from src.ui.text_input import TextInput

from src.ui.region.region_labels import (
    get_region_type_label
)

class RegionForm(BaseForm):
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
            "Nome da região"
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
            "Descrição da região..."
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
            "Criar Região"
        )
        
        self.mode = "create"
        self.editing_region_id = None
        
        self.fields = [
            self.name_input,
            self.description_input,
            self.notes_input
        ]
        
        self.region_types = list(
            RegionType
        )
        
        self.region_type_index = (
            self.region_types.index(
                RegionType.OTHER
            )
        )
        
    @property
    def selected_region_type(self):
        return self.region_types[
            self.region_type_index
        ]
             
    def _update_type_button(self):
        self.type_button.text = (
            get_region_type_label(
                self.selected_region_type
            )
        )
        
    def _next_region_type(self):
        self.region_type_index = (
            self.region_type_index + 1
        ) % len(self.region_types)
        
        self._update_type_button()
        
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
            
        if self.type_button.handle_event(
            event
        ):
            self._next_region_type()
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
                "O nome da região é obrigatório."
            )
            
            return False
        
        return True
            
    def build_region(
        self,
        world_id: int
    ):
        if not self.validate():
            return None
        
        return Region(
            id=self.editing_region_id,
            world_id=world_id,
            name=self.name_input.text.strip(),
            region_type=(
                self.selected_region_type
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
        
    def prepare_create(self):
        super().prepare_create()
        
        self.mode = "create"
        self.editing_region_id = None
        
        self.region_type_index = (
            self.region_types.index(
                RegionType.OTHER
            )
        )
        
        self._update_type_button()      
        self.submit_button.text = (
            "Criar Região"
        )
        
    def prepare_edit(
        self,
        region
    ):
        self.clear()
        
        self.mode = "edit"
        self.editing_region_id = region.id
        
        self.name_input.text = region.name
        self.name_input.cursor_index = len(
            region.name
        )
        
        self.description_input.text = (
            region.description
        )
        self.description_input.cursor_index = len(
            region.description
        )
        
        self.notes_input.text = (
            region.notes
        )
        self.notes_input.cursor_index = len(
            region.notes
        )
        
        self.region_type_index = (
            self.region_types.index(
                region.region_type
            )
        )
        
        self._update_type_button()
        
        self.submit_button.text = "Salvar"
        
        self._set_focus(0)
        
    def render(self, screen):
        title = self.title_font.render(
            "Nova Região",
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

        type_label = self.info_font.render(
            "Tipo",
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

    def build_campaign_region(
        self,
        campaign_id
    ):
        return CampaignRegion(
            campaign_id=campaign_id,
            name=self.name_input.text.strip(),
            region_type=self.selected_region_type,
            description=self.description_input.text.strip(),
            notes=self.notes_input.text.strip(),
        )

