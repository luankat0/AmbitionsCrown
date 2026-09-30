import pygame

from src.models.npc import NPC
from src.ui.button import Button

class NPCDetailsView:
    def __init__(self):
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None,
            26
        )
        
        self.back_button = Button(
            280,
            110,
            120,
            45,
            "Voltar"
        )
        
        self.edit_button = Button(
            420,
            110,
            120,
            45,
            "Editar"
        )
        
        self.delete_button = Button(
            560,
            110,
            120,
            45,
            "Excluir"
        )
        
    def handle_event(self, event):
        if self.back_button.handle_event(event):
            return "back"
        
        if self.edit_button.handle_event(event):
            return "edit"
        
        if self.delete_button.handle_event(event):
            return "delete"

        return None
    
    def render(
        self,
        screen,
        npc: NPC
    ):
        title = self.title_font.render(
            npc.name,
            True,
            (240, 240, 240)
        )
        
        screen.blit(
            title,
            (280, 40)
        )
        
        self.back_button.render(screen)
        self.edit_button.render(screen)
        self.delete_button.render(screen)
        
        self._render_basic_info(
            screen,
            npc
        )
        
        self._render_description(
            screen,
            npc
        )
        
        self._render_personality(
            screen,
            npc
        )
        
        self._render_notes(
            screen,
            npc
        )
        
    def _render_basic_info(
        self,
        screen,
        npc: NPC
    ):
        info_x = 300
        info_y = 190
        
        basic_info = [
            ("Raça", npc.race),
            ("Função", npc.role),
            ("Região", npc.region)
        ]
        
        for label, value in basic_info:
            label_surface = self.info_font.render(
                f"{label}:",
                True,
                (160, 160, 175)
            )
            
            value_surface = self.info_font.render(
                value if value else "-",
                True,
                (230, 230, 235)
            )
            
            screen.blit(
                label_surface,
                (info_x, info_y)
            )
            
            screen.blit(
                value_surface,
                (info_x + 100, info_y)
            )
            
            info_y += 40
        
    def _render_description(
        self,
        screen,
        npc: NPC
    ):
        title = self.info_font.render(
            "Descrição",
            True,
            (180, 180, 200)
        )
        
        screen.blit(
            title,
            (300, 340)
        )
        
        self._draw_wrapped_text(
            screen,
            npc.description,
            300,
            375,
            380,
            (220, 220, 225)
        )
        
    def _render_personality(
        self,
        screen,
        npc: NPC
    ):
        title = self.info_font.render(
            "Personalidade",
            True,
            (180, 180, 200)
        )
        
        screen.blit(
            title,
            (750, 190)
        )
        
        self._draw_wrapped_text(
            screen,
            npc.personality,
            750,
            225,
            400,
            (220, 220, 225)
        )
        
    def _render_notes(
        self,
        screen,
        npc: NPC
    ):
        title = self.info_font.render(
            "Observações do Mestre",
            True,
            (180, 180, 200)
        )
        
        screen.blit(
            title,
            (750, 390)
        )
        
        self._draw_wrapped_text(
            screen,
            npc.notes,
            750,
            425,
            400,
            (220, 220, 225)
        )
        
    def _draw_wrapped_text(
        self, 
        screen, 
        text, 
        x, 
        y, 
        max_width, 
        color
    ):
        if not text:
            text = "-"
            
        paragraphs = text.split("\n")
        
        for paragraph in paragraphs:
            words = paragraph.split(" ")
            
            line = ""
            
            for word in words:
                test_line = line
                
                if test_line:
                    test_line += " "
                
                test_line += word
                
                width, _ = self.info_font.size(
                    test_line
                )
                
                if width <= max_width:
                    line = test_line
                    
                else:
                    if line:
                        surface = self.info_font.render(
                            line,
                            True,
                            color
                        )
                        
                        screen.blit(
                            surface,
                            (x, y)
                        )
                        
                        y += (
                            self.info_font
                            .get_linesize()
                        )
                        
                    line = word
                    
            if line:
                surface = self.info_font.render(
                    line, 
                    True,
                    color
                )
                
                screen.blit(
                    surface,
                    (x, y)
                )    

                y += self.info_font.get_linesize()
                
            y += 5
        
        return y