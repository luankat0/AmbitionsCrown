import pygame

from src.ui.button import Button

from src.ui.region.region_labels import (
    get_region_type_label
)

from src.ui.location.location_tree_view import (
    LocationTreeView
)

class RegionDetailsView:
    def __init__(self):
        self.name_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.back_button = Button(
            300,
            120,
            140,
            45,
            "← Voltar"
        )
        
        self.new_location_button = Button(
            720,
            520,
            180,
            45,
            "+ Novo Local"
        )
        self.edit_button = Button(
            940,
            200,
            180,
            45,
            "Editar Região"
        )
        
        self.delete_button = Button(
            940,
            255,
            180,
            45,
            "Excluir Região"
        )
        
        self.location_tree_view = (
            LocationTreeView()
        )
        
    def handle_event(
        self,
        event
    ):
        if self.back_button.handle_event(
            event
        ):
            return "back", None
        
        if self.edit_button.handle_event(
            event
        ):
            return "edit_region", None
        
        if self.delete_button.handle_event(
            event
        ):
            return "delete_region", None
        
        if self.new_location_button.handle_event(
            event
        ):
            return "new_location", None
        
        location = (
            self.location_tree_view
            .handle_event(
                event
            )
        )
        
        if location is not None:
            return "select_location", location
        
        return None, None
    
    def render(
        self,
        screen,
        region,
        locations
    ):
        self.back_button.render(
            screen
        )
        
        self.edit_button.render(
            screen
        )
        
        self.delete_button.render(
            screen
        )
        
        name_surface = (
            self.name_font.render(
                region.name,
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            name_surface,
            (300, 200)
        )
        
        type_text = (
            get_region_type_label(
                region.region_type
            )
        )
        
        type_surface = (
            self.info_font.render(
                type_text,
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            type_surface,
            (300, 250)
        )
        
        self._render_description(
            screen,
            region
        )
        
        self._render_notes(
            screen,
            region
        )
        
        self._render_locations_section(
            screen,
            locations
        )
        
    def _render_description(
        self,
        screen,
        region
    ):
        label_surface = (
            self.info_font.render(
                "Descrição",
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            label_surface,
            (300, 320)
        )
        
        description = (
            region.description.strip()
        )
        
        if not description:
            description = "Sem descrição."
            
        description_surface = (
            self.info_font.render(
                description,
                True,
                (190, 190, 200)
            )
        )
        
        screen.blit(
            description_surface,
            (300, 355)
        )
        
    def _render_notes(
        self,
        screen,
        region
    ):
        label_surface = (
            self.info_font.render(
                "Anotações do Mestre",
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            label_surface,
            (300, 410)
        )
        
        notes = region.notes.strip()
        
        if not notes:
            notes = "Sem anotações."
            
        notes_surface = (
            self.info_font.render(
                notes,
                True,
                (190, 190, 200)
            )
        )
        
        screen.blit(
            notes_surface,
            (300, 455)
        )
        
    def _render_locations_section(
        self,
        screen,
        locations
    ):
        title_surface = (
            self.name_font.render(
                "Locais",
                True,
                (235, 235, 240)
            )
        )
        
        self.new_location_button.render(
            screen
        )
        
        screen.blit(
            title_surface,
            (300, 520)
        )
        
        self.location_tree_view.render(
            screen,
            locations,
            start_x=300,
            start_y=575
        )
