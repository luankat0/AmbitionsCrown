import pygame

from src.models.region import RegionType

from src.ui.button import Button

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
        
    def handle_event(
        self,
        event
    ):
        if self.back_button.handle_event(
            event
        ):
            return "back"
        
        return None
    
    def render(
        self,
        screen,
        region
    ):
        self.back_button.render(
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
            self._get_region_type_label(
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
            screen
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
            (300, 300)
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
            (300, 330)
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
            (300, 300)
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
            (300, 410)
        )
        
    def _render_locations_section(
        self,
        screen
    ):
        title_surface = (
            self.name_font.render(
                "Locais",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            title_surface,
            (300, 480)
        )
        
        placeholder_surface = (
            self.info_font.render(
                "Os locais desta região aparecerão aqui.",
                True,
                (150, 150, 100)
            )
        )
        
        screen.blit(
            placeholder_surface,
            (300, 535)
        )
        
    def _get_region_type_label(
        self,
        region_type: RegionType
    ):
        labels = {
            RegionType.KINGDOM:
            "Reino",

            RegionType.PROVINCE:
                "Província",

            RegionType.TERRITORY:
                "Território",

            RegionType.FOREST:
                "Floresta",

            RegionType.DESERT:
                "Deserto",

            RegionType.MOUNTAINS:
                "Montanhas",

            RegionType.ISLAND:
                "Ilha",

            RegionType.OTHER:
                "Outro",
        }
        
        return labels.get(
            region_type,
            region_type.value
        )