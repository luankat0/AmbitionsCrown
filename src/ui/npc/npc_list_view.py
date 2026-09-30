import pygame

from src.models.npc import NPC
from src.ui.button import Button

class NPCListView:
    def __init__(self):
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.info_font = pygame.font.Font(
            None, 
            26
        )
        
        self.new_npc_button = Button(
            280,
            110,
            160,
            45,
            "+ Novo NPC"
        )
        
        self.npc_rects = {}
        
    def handle_event(
        self,
        event,
        npcs: list[NPC]
    ):
        if self.new_npc_button.handle_event(event):
            return "create", None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                for npc in npcs:
                    if npc.id is None:
                        continue
                    
                    rect = self.npc_rects.get(
                        npc.id
                    )
                    
                    if (
                        rect
                        and rect.collidepoint(event.pos)
                    ):
                        return "select", npc
        return None, None
    
    def render(
        self,
        screen,
        npcs: list[NPC]
    ):
        self.npc_rects.clear()
        
        title = self.title_font.render(
            "NPCs",
            True,
            (240, 240, 240)
        )
        
        screen.blit(
            title,
            (280, 40)
        )
        
        self.new_npc_button.render(screen)
        
        list_rect = pygame.Rect(
            280,
            190,
            900,
            450
        )
        
        pygame.draw.rect(
            screen,
            (36, 36, 44),
            list_rect,
            border_radius=8
        )
        
        if not npcs:
            empty_text = self.info_font.render(
                "Nenhum NPC criado ainda.",
                True,
                (150, 150, 160)
            )
            
            screen.blit(
                empty_text,
                (310, 220)
            )
            
            return
        
        y = 220
        
        for npc in npcs:
            card_rect = pygame.Rect(
                300,
                y,
                840,
                65
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                card_rect,
                border_radius=6
            )
            
            if npc.id is not None:
                self.npc_rects[npc.id] = (
                    card_rect
                )
                
            name_surface = (
                self.info_font.render(
                    npc.name,
                    True,
                    (235, 235, 240)
                )
            )
            
            screen.blit(
                name_surface,
                (
                    card_rect.x + 15,
                    card_rect.y + 10
                )
            )
            
            details_surface = (
                self.info_font.render(
                    npc.get_summary(),
                    True,
                    (155, 155,165)
                )
            )
            
            screen.blit(
                details_surface,
                (
                    card_rect.x + 15,
                    card_rect.y + 35
                )
            )
            
            y += 80