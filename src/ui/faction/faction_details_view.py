import pygame

from src.ui.button import Button
from src.ui.faction.faction_labels import (
    get_faction_status_label,
    get_faction_type_label
)


class FactionDetailsView:
    def __init__(self):
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.label_font = pygame.font.Font(
            None,
            24
        )
        
        self.text_font = pygame.font.Font(
            None,
            22
        )
        
        self.back_button = Button(
            300,
            70,
            120,
            40,
            "Voltar"
        )
        
        self.edit_button = Button(
            940,
            160,
            180,
            45,
            "Editar Facção"
        )
        
        self.delete_button = Button(
            940,
            215,
            180,
            45,
            "Excluir Facção"
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
            return "edit", None

        if self.delete_button.handle_event(
            event
        ):
            return "delete", None
        
        return None, None
    
    def render(
        self,
        screen,
        faction
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
        
        title_surface = (
            self.title_font.render(
                faction.name,
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            title_surface,
            (300, 130)
        )
        
        type_label = (
            self.label_font.render(
                "Tipo",
                True,
                (150, 150, 165)
            )
        )
        
        type_value = (
            self.text_font.render(
                get_faction_type_label(
                    faction.faction_type
                ),
                True,
                (220, 220, 230)
            )
        )
        
        status_label = (
            self.label_font.render(
                "Status",
                True,
                (150, 150, 165)
            )
        )
        
        status_value = (
            self.text_font.render(
                get_faction_status_label(
                    faction.status
                ),
                True,
                (220, 220, 230)
            )
        )
        
        screen.blit(
            type_label,
            (300, 210)
        )
        
        screen.blit(
            type_value,
            (300, 240)
        )
        
        screen.blit(
            status_label,
            (520, 210)
        )
        
        screen.blit(
            status_value,
            (520, 240)
        )
        
        self._render_text_section(
            screen,
            "Descrição",
            faction.description,
            300,
            310,
            600
        )
        
        self._render_text_section(
            screen,
            "Anotações do Mestre",
            faction.notes,
            300,
            470,
            600
        )
        
    def _render_text_section(
        self,
        screen,
        title,
        text,
        x,
        y,
        max_width
    ):
        title_surface = (
            self.label_font.render(
                title,
                True,
                (150, 150, 165)
            )
        )
        
        screen.blit(
            title_surface,
            (x, y)
        )
        
        content = text.strip()
        
        if not content:
            content = "Nenhuma informação registrada."
            
        lines = self._wrap_text(
            content,
            max_width
        )
        
        line_y = y + 35
        
        for line in lines:
            line_surface = (
                self.text_font.render(
                    line,
                    True,
                    (210, 210, 220)
                )
            )
            
            screen.blit(
                line_surface,
                (x, line_y)
            )
            
            line_y += 25
            
    def _wrap_text(
        self,
        text,
        max_width
    ):
        lines = []
        
        for paragraph in text.splitlines():
            if not paragraph:
                lines.append("")
                continue
            
            words = paragraph.split()
            current_line = ""
            
            for word in words:
                test_line = (
                    word
                    if not current_line
                    else f"{current_line} {word}"
                )
                
                width = (
                    self.text_font.size(
                        test_line
                    )[0]
                )
                
                if width <= max_width:
                    current_line = test_line
                    continue
                
                if current_line:
                    lines.append(
                        current_line
                    )
                    
            if current_line:
                lines.append(
                    current_line
                )
                
        return lines
            