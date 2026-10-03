import pygame

from src.ui.button import Button

from src.ui.location.location_children_view import (
    LocationChildrenView
)
from src.ui.location.location_labels import (
    get_location_type_label
)


class LocationDetailsView:
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
        
        self.new_child_button = Button(
            720,
            520,
            200,
            45,
            "+ Novo Sublocal"
        )
        
        self.edit_button = Button(
            940,
            200,
            180,
            45,
            "Editar Local"
        )
        
        self.children_view = LocationChildrenView()

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
            return "edit_location", None
        
        if self.new_child_button.handle_event(
            event
        ):
            return "new_child", None
        
        child = (
            self.children_view
            .handle_event(
                event
            )
        )
        
        if child is not None:
            return "open_child", child

        return None, None

    def render(
        self,
        screen,
        location,
        children
    ):
        self.back_button.render(
            screen
        )
        
        self.edit_button.render(
            screen
        )

        name_surface = (
            self.name_font.render(
                location.name,
                True,
                (235, 235, 240)
            )
        )

        screen.blit(
            name_surface,
            (300, 200)
        )

        type_text = (
            get_location_type_label(
                location.location_type
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
            location
        )

        self._render_notes(
            screen,
            location
        )

        self._render_children_section(
            screen,
            children
        )
        
    def _render_description(
        self,
        screen,
        location
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
            location.description.strip()
        )
        
        if not description:
            description = "Sem descrição"
            
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
        location
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
        
        notes = location.notes.strip()
        
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
            (300, 445)
        )
        
    def _render_children_section(
        self,
        screen,
        children
    ):
        title_surface = (
            self.name_font.render(
                "Sublocais",
                True,
                (235, 235, 240)
            )
        )
        
        self.new_child_button.render(
            screen
        )

        screen.blit(
            title_surface,
            (300, 520)
        )

        self.children_view.render(
            screen,
            children,
            start_x=300,
            start_y=575
        )
