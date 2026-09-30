import pygame

from src.ui.confirm_dialog import ConfirmDialog

from src.ui.npc.npc_form import NPCForm
from src.ui.npc.npc_list_view import NPCListView
from src.ui.npc.npc_details_view import NPCDetailsView

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
        self.list_view = NPCListView()
        self.details_view = NPCDetailsView()
        
        self.confirm_dialog = ConfirmDialog()

        self.show_form = False
        self.selected_npc = None

        self.repository = self.app.npc_repository
        
        self.npcs = self.repository.get_all()
        
    def handle_event(self, event):
        if self.confirm_dialog.visible:
            self.handle_confirm_dialog_events(
                event
            )
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                
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
        action, npc = self.list_view.handle_event(
            event,
            self.npcs
        )
        
        if action == "create":
            self.selected_npc = None
            
            self.form.prepare_create()
        
            self.show_form = True
            return
        
        if action == "select":
            self.selected_npc = npc
            
    def handle_detail_events(self, event):
        action = self.details_view.handle_event(
            event
        )
        
        if action == "back":
            self.selected_npc = None
            return
        
        if action == "edit":
            self.open_edit_form()
            return
        
        if action == "delete":
            self.open_delete_confirmation()
            return
        
    def handle_confirm_dialog_events(self, event):
        action = self.confirm_dialog.handle_event(
            event
        )
        
        if action == "cancel":
            self.confirm_dialog.close()
            return
        
        if action == "confirm":
            self.delete_selected_npc()
        
    def render(self, screen):
        super().render(screen)

        if self.show_form:
            self.form.render(screen)
            
        elif self.selected_npc is not None:
            self.details_view.render(
                screen,
                self.selected_npc
            )
            
        else:
            self.list_view.render(
                screen,
                self.npcs
            )
            
        self.confirm_dialog.render(screen)
               
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
        self.confirm_dialog.close()
     
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
             
    def open_delete_confirmation(self):
        npc = self.selected_npc
        
        if npc is None:
            return
        
        self.confirm_dialog.open(
            title="Excluir NPC?",
            message=(
                f"Tem certeza que deseja excluir {npc.name}?"
            ),
            warning=(
                "Esta ação não poderá ser desfeita."
            ),
            confirm_text="Excluir"
        )

