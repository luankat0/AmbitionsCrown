import pygame

from src.models.npc import NPC

from src.screens.base_screen import BaseScreen

from src.ui.button import Button
from src.ui.text_input import TextInput
from src.ui.text_area import TextArea

class NPCScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(
            app,
            "npcs"
        )

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

        self.show_form = False
        
        self.selected_npc = None
        
        self.npc_rects = {}
        
        self.back_button = Button(
            280,
            110,
            120,
            45,
            "Voltar"
        )

        self.repository = self.app.npc_repository
        
        self.npcs = self.repository.get_all()
        
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
            "Profissão ou função"
        )

        self.region_input = TextInput(
            420,
            360,
            280,
            42,
            "Região"
        )
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
        
        self.cancel_button = Button(
            800,
            590,
            140,
            45,
            "Cancelar"
        )
        
        self.create_button = Button(
            960,
            590,
            160,
            45,
            "Criar NPC"
        )
        
    def handle_event(self, event):
        super().handle_event(event)
        
        if self.show_form:
            self.handle_form_events(event)
            
        elif self.selected_npc is not None:
            self.handle_detail_events(event)
        
        else:
            self.handle_list_events(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
                if self.show_form:
                    self.show_form = False
                    
                elif self.selected_npc is not None:
                    self.selected_npc = None
                    
                else:
                    self.app.change_screen("dashboard")

    def handle_form_events(self, event):
        self.name_input.handle_event(event)
        self.race_input.handle_event(event)
        self.role_input.handle_event(event)
        self.region_input.handle_event(event)
        
        self.description_input.handle_event(event)
        self.personality_input.handle_event(event)
        self.notes_input.handle_event(event)
        
        if self.cancel_button.handle_event(event):
            self.show_form = False
        
        if self.create_button.handle_event(event):
            self.create_npc()
    
    def handle_list_events(self, event):
        if self.new_npc_button.handle_event(event):
            self.show_form = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                for npc in self.npcs:
                    if npc.id is None:
                        continue
                    
                    rect = self.npc_rects.get(npc.id)
                    
                    if rect and rect.collidepoint(event.pos):
                        self.selected_npc = npc
                        return
    
    def handle_detail_events(self, event):
        if self.back_button.handle_event(event):
            self.selected_npc = None
        
    def render(self, screen):
        super().render(screen)

        if self.show_form:
            self.render_form(screen)
            
        elif self.selected_npc is not None:
            self.render_npc_details(screen)
            
        else:
            self.render_npc_list(screen)
        
    def render_form(self, screen):
        title = self.title_font.render(
            "Criar NPC",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title,
            (280, 40)
        )

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

        self.name_input.render(screen)
        self.race_input.render(screen)
        self.role_input.render(screen)
        self.region_input.render(screen)

        self.description_input.render(screen)
        self.personality_input.render(screen)
        self.notes_input.render(screen)

        self.cancel_button.render(screen)
        self.create_button.render(screen)
        
    def render_npc_list(self, screen):
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

        if not self.npcs:
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
        
        self.npc_rects.clear()

        y = 220

        for npc in self.npcs:
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
                self.npc_rects[npc.id] = card_rect
                
            name_surface = self.info_font.render(
                npc.name,
                True,
                (235, 235, 240)
            )
            
            screen.blit(
                name_surface,
                (card_rect.x + 15, card_rect.y + 10)
            )
            
            details_surface = self.info_font.render(
                npc.get_summary(),
                True,
                (155, 155, 165)
            )
            
            screen.blit(
                details_surface,
                (card_rect.x + 15, card_rect.y + 35)
            )
            
            y += 80
    
    def render_npc_details(self, screen):
        npc = self.selected_npc
        
        if npc is None:
            return
        
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
        
        info_x = 300
        info_y = 190
        
        basic_info = [
            ("Raça", npc.race),
            ("Função", npc.role),
            ("Região", npc.region),
        ]
        
        description_title = self.info_font.render(
            "Descrição",
            True,
            (180, 180, 200)
        )
        
        screen.blit(
            description_title,
            (300, 340)
        )
        
        self.draw_wrapped_text(
            screen,
            npc.description,
            300,
            375,
            380,
            (220, 220, 225)
        )
        
        personality_title = self.info_font.render(
            "Personalidade",
            True,
            (180, 180, 200)
        )

        screen.blit(
            personality_title,
            (750, 190)
        )

        self.draw_wrapped_text(
            screen,
            npc.personality,
            750,
            225,
            400,
            (220, 220, 225)
        )
        
        notes_title = self.info_font.render(
            "Observações do Mestre",
            True,
            (180, 180, 200)
        )

        screen.blit(
            notes_title,
            (750, 390)
        )

        self.draw_wrapped_text(
            screen,
            npc.notes,
            750,
            425,
            400,
            (220, 220, 225)
        )
        
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
            
    def create_npc(self):
        if not self.name_input.text.strip():
            return
        
        npc = NPC(
            name=self.name_input.text.strip(),
            race=self.race_input.text.strip(),
            role=self.role_input.text.strip(),
            region=self.region_input.text.strip(),
            description=self.description_input.text.strip(),
            personality=self.personality_input.text.strip(),
            notes=self.notes_input.text.strip()
        )
        
        self.repository.add(npc)
        
        self.npcs.insert(
            0,
            npc
        )
        
        self.clear_form()
        
        self.show_form = False
        
    def clear_form(self):
        
        self.name_input.text = ""
        self.race_input.text = ""
        self.role_input.text = ""
        self.region_input.text = ""
        
        self.description_input.text = ""
        self.personality_input.text = ""
        self.notes_input.text = ""
        
        
    def draw_wrapped_text(
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