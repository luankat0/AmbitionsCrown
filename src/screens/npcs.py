import pygame

from src.models.npc import NPC
from src.ui.button import Button
from src.ui.npc.npc_form import NPCForm
from src.screens.base_screen import BaseScreen

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
        
        self.form = NPCForm()

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
        
        self.edit_button = Button(
            420,
            110,
            120,
            45,
            "Editar"
        )

        self.repository = self.app.npc_repository
        
        self.npcs = self.repository.get_all()
        
        self.show_delete_confirmation = False
        
        self.delete_button = Button(
            560,
            110,
            120,
            45,
            "Excluir"
        )
        
        self.delete_cancel_button = Button(
            500, 
            400, 
            140, 
            45, 
            "Cancelar"
        )
        
        self.delete_confirm_button = Button(
            660,
            400,
            140,
            45,
            "Excluir"
        )
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
                # Modal de exclusão aberto
                # ESC apenas fecha o modal
                if self.show_delete_confirmation:
                    self.show_delete_confirmation = False
                    return
                
                # Formulário aberto:
                # ESC cancela o formulário
                if self.show_form:
                    self.form.clear()
                    self.show_form = False
                    return
                
                # Detalhes de NPC abertos:
                # ESC volta para a lista
                if self.selected_npc is not None:
                    self.selected_npc = None
                    return
                
                # ESC volta ao Dashboard.
                self.app.change_screen("dashboard")
                return
        
        # Se o modal estiver aberto,
        # nenhum outro componente recebe eventos
        if self.show_delete_confirmation:
            self.handle_delete_confirmation_events(event)
            return
        
        # Sidebar e comportamento padrão da tela
        super().handle_event(event)
        
        if self.show_form:
            self.handle_form_events(event)
            
        elif self.selected_npc is not None:
            self.handle_detail_events(event)
        
        else:
            self.handle_list_events(event)

    def handle_form_events(self, event):
        action = self.form.handle_event(event)
        
        if action == "cancel":
            self.form.clear()
            self.show_form = False
            return
        
        if action == "submit":
            self.submit_form()
    
    def handle_list_events(self, event):
        if self.new_npc_button.handle_event(event):            
            self.selected_npc = None
            
            self.form.prepare_create()
                        
            self.show_form = True
            return
        
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
            self.show_delete_confirmation = False
            self.selected_npc = None
            return

        if self.edit_button.handle_event(event):
            self.open_edit_form()
            return
            
        if self.delete_button.handle_event(event):
            self.show_delete_confirmation = True
            return
        
    def handle_delete_confirmation_events(self, event):
        if self.delete_cancel_button.handle_event(event):
            self.show_delete_confirmation = False
            return
        
        if self.delete_confirm_button.handle_event(event):
            self.delete_selected_npc()
        
    def render(self, screen):
        super().render(screen)

        if self.show_form:
            self.form.render(screen)
            
        elif self.selected_npc is not None:
            self.render_npc_details(screen)
            
        else:
            self.render_npc_list(screen)
            
        if self.show_delete_confirmation:
            self.render_delete_confirmation(screen)
        
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
        self.edit_button.render(screen)
        self.delete_button.render(screen)
        
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
    
    def render_delete_confirmation(self, screen):
        npc = self.selected_npc
        
        if npc is None:
            return
        
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )
        
        overlay.fill(
            (0, 0, 0, 150)
        )
        
        screen.blit(
            overlay,
            (0, 0)
        )
        
        modal_rect = pygame.Rect(
            420,
            250,
            480,
            240
        )
        
        pygame.draw.rect(
            screen,
            (36, 36, 44),
            modal_rect,
            border_radius=10
        )
        
        pygame.draw.rect(
            screen,
            (90, 90, 105),
            modal_rect,
            width=2,
            border_radius=10
        )
        
        title = self.title_font.render(
            "Excluir NPC?",
            True,
            (240, 240, 240)
        )
        
        screen.blit(
            title,
            (modal_rect.x + 30, modal_rect.y + 25)
        )
        
        message = (
            f"Tem certeza que deseja excluir {npc.name}?"
        )
        
        message_surface = self.info_font.render(
            message,
            True,
            (210, 210, 220)
        )
        
        screen.blit(
            message_surface,
            (modal_rect.x + 30, modal_rect.y + 90)
        )
        
        warning_surface = self.info_font.render(
            "Esta ação não poderá ser desfeita.",
            True,
            (170, 170, 180)
        )
        
        screen.blit(
            warning_surface,
            (modal_rect.x + 30, modal_rect.y + 125)
        )
        
        self.delete_cancel_button.render(screen)
        self.delete_confirm_button.render(screen)
            
    def create_npc(self):
        npc = self.form.build_npc()
        
        if npc is None:
            return
        
        self.repository.add(npc)
        
        self.npcs.insert(
            0,
            npc
        )
        
        self.form.clear()
        self.show_form = False
    
    def update_npc(self):
        selected_npc = self.selected_npc
        
        if selected_npc is None:
            return
        
        form_npc = self.form.build_npc()
        
        if form_npc is None:
            return
        
        selected_npc.name = form_npc.name
        selected_npc.race = form_npc.race
        selected_npc.role = form_npc.role
        selected_npc.region = form_npc.region

        selected_npc.description = form_npc.description
        selected_npc.personality = form_npc.personality
        selected_npc.notes = form_npc.notes

        self.repository.update(selected_npc)

        self.form.clear()
        self.show_form = False
    
    def delete_selected_npc(self):
        npc = self.selected_npc
        
        if npc is None:
            return
        
        self.repository.delete(npc)
        
        self.npcs = [
            item
            for item in self.npcs
            if item.id != npc.id
        ]
        
        self.selected_npc = None
        self.show_delete_confirmation = False
     
    def open_edit_form(self):
        npc = self.selected_npc
        
        if npc is None:
            return
        
        self.form.load_npc(npc)
        
        self.show_form = True
      
    def submit_form(self):
        if self.form.mode == "create":
            self.create_npc()
            
        elif self.form.mode == "edit":
            self.update_npc()
             
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
    
    