import pygame

from src.screens.base_screen import BaseScreen
from src.ui.button import Button
from src.ui.text_input import TextInput

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

        self.npcs = [] # Armazenamento em memória (temporário)

        self.name_input = TextInput(
            500,
            150,
            400,
            42,
            "Nome do NPC"
        )  

        self.race_input = TextInput(
            500, 
            220, 
            400, 
            42, 
            "Raça"
        )      

        self.role_input = TextInput(
            500,
            290,
            400,
            42,
            "Profissão ou função"
        )
        
        self.region_input = TextInput(
            500,
            360,
            400,
            42,
            "Região"
        )
        
        self.cancel_button = Button(
            500,
            440,
            140,
            45,
            "Cancelar"
        )
        
        self.create_button = Button(
            660,
            440,
            160,
            45,
            "Criar NPC"
        )
        
    def handle_event(self, event):
        super().handle_event(event)
        
        if self.show_form:
            self.handle_form_events(event)
        
        else:
            if self.new_npc_button.handle_event(event):
                self.show_form = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.show_form:
                    self.show_form = False
                else:
                    self.app.change_screen("dashboard")

    def render(self, screen):
        super().render(screen)

        if self.show_form:
            self.render_form(screen)
            
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

        labels = [
            ("Nome", 150),
            ("Raça", 220),
            ("Função", 290),
            ("Região", 360),
        ]

        for label, y in labels:
            label_surface = self.info_font.render(
                label,
                True,
                (200, 200, 210)
            )

            screen.blit(
                label_surface,
                (300, y + 10)
            )

        self.name_input.render(screen)
        self.race_input.render(screen)
        self.role_input.render(screen)
        self.region_input.render(screen)

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

        y = 220

        for npc in self.npcs:
            name = self.info_font.render(
                npc["name"],
                True,
                (235, 235, 240)
            )

            screen.blit(
                name,
                (310, y)
            )

            details = (
                f'{npc["race"]} • '
                f'{npc["role"]} • '
                f'{npc["region"]}'
            )

            details_surface = self.info_font.render(
                details,
                True,
                (155, 155, 165)
            )

            screen.blit(
                details_surface,
                (310, y + 28)
            )

            y += 80
        
    def handle_form_events(self, event):
        self.name_input.handle_event(event)
        self.race_input.handle_event(event)
        self.role_input.handle_event(event)
        self.region_input.handle_event(event)
        
        if self.cancel_button.handle_event(event):
            self.show_form = False
        
        if self.create_button.handle_event(event):
            self.create_npc()
            
    def create_npc(self):
        if not self.name_input.text.strip():
            return
        
        npc = {
            "name": self.name_input.text.strip(),
            "race": self.race_input.text.strip(),
            "role": self.role_input.text.strip(),
            "region": self.region_input.text.strip()
        }
        
        self.npcs.append(npc)
        
        self.clear_form()
        
        self.show_form = False
        
    def clear_form(self):
        self.name_input.text = ""
        self.race_input.text = ""
        self.role_input.text = ""
        self.region_input.text = ""