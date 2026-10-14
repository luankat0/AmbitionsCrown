import pygame
import sqlite3

from enum import Enum, auto

from src.ui.button import Button

from src.ui.dialogs.confirm_dialog import ConfirmDialog
from src.ui.dialogs.message_dialog import MessageDialog

from src.ui.faction.faction_labels import (
    get_faction_type_label,
    get_faction_status_label,
)
from src.ui.faction.faction_form import FactionForm

class WorldFactionViewMode(Enum):
    DETAILS = auto()
    EDIT_FORM = auto()


class WorldFactionScreen:
    def __init__(self, app, world, faction):
        self.app = app
        self.world = world
        self.faction = faction

        self.background_color = (30, 30, 35)

        self.title_font = pygame.font.Font(None, 48)
        self.name_font = pygame.font.Font(None, 34)
        self.info_font = pygame.font.Font(None, 24)

        self.back_button = Button(
            80, 110,
            220, 45,
            "Voltar às Facções"
        )
        
        self.view_mode = WorldFactionViewMode.DETAILS
        
        self.faction_form = FactionForm()
        
        self.edit_button = Button(
            330, 110,
            190, 45,
            "Editar Facção"
        )
        
        self.delete_button = Button(
            550, 110,
            190, 45,
            "Excluir Facção"
        )
        
        self.confirm_dialog = ConfirmDialog()
        
        self.message_dialog = MessageDialog(
            "",
            ""
        )

        self.content_rect = pygame.Rect(
            80, 175, 1080, 485
        )

        self.scroll_offset = 0
        self.scroll_speed = 40
        self.content_height = 0

    def handle_event(self, event):
        
        # Diálogo de Mensagem
        if self.message_dialog.visible:
            self.message_dialog.handle_event(event)
            return
        
        # Diálogo de confirmação
        if self.confirm_dialog.visible:
            action = self.confirm_dialog.handle_event(event)
            
            if action == "cancel":
                self.confirm_dialog.close()
                return
            
            if action == "confirm":
                self.confirm_delete_faction()
                return
            
            return
        
        # Tratamento do ESC
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == WorldFactionViewMode.EDIT_FORM
            ):
                self.cancel_edit()
                return
            
            self.return_to_factions()
            return
        
        if (
            self.view_mode
            == WorldFactionViewMode.EDIT_FORM
        ):
            self.handle_edit_form_events(event)
            return
        
        # Voltar à lista
        if self.back_button.handle_event(event):
            self.return_to_factions()
            return

        # Editar Facção
        if self.edit_button.handle_event(event):
            self.faction_form.prepare_edit(
                self.faction
            )
            
            self.view_mode = (
                WorldFactionViewMode.EDIT_FORM
            )
            return
        
        # Excluir Facção
        if self.delete_button.handle_event(event):
            self.request_delete_faction()
            return
        
        # Scroll dos detalhes
        if event.type == pygame.MOUSEWHEEL:
            if self.content_rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.scroll_offset -= (
                    event.y * self.scroll_speed
                )

                self._clamp_scroll()

    def return_to_factions(self):
        self.app.open_world_factions(
            self.world
        )

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.background_color)
        
        if (
            self.view_mode
            == WorldFactionViewMode.EDIT_FORM
        ):
            self.faction_form.render(screen)
            return

        title = self.title_font.render(
            "Detalhes da Facção",
            True,
            (240, 240, 245)
        )

        screen.blit(title, (80, 55))

        self.back_button.render(screen)
        
        self.edit_button.render(screen)
        
        self.delete_button.render(screen)

        previous_clip = screen.get_clip()
        screen.set_clip(self.content_rect)

        content_top = (
            self.content_rect.y
            + 10
            - self.scroll_offset
        )

        y = content_top

        # Mundo ao qual a facção pertence
        world_text = self.info_font.render(
            f"Mundo: {self.world.name}",
            True,
            (165, 150, 185)
        )

        screen.blit(world_text, (80, y))
        y += 45

        # Nome da facção
        name = self.title_font.render(
            self.faction.name,
            True,
            (230, 220, 245)
        )

        screen.blit(name, (80, y))
        y += 70

        # Tipo
        faction_type = get_faction_type_label(
            self.faction.faction_type
        )

        type_text = self.info_font.render(
            f"Tipo: {faction_type}",
            True,
            (210, 210, 220)
        )

        screen.blit(type_text, (80, y))
        y += 35

        # Status
        faction_status = get_faction_status_label(
            self.faction.status
        )

        status_text = self.info_font.render(
            f"Status: {faction_status}",
            True,
            (210, 210, 220)
        )

        screen.blit(status_text, (80, y))
        y += 65

        # Descrição
        y = self.render_text_section(
            screen,
            "Descrição",
            self.faction.description,
            y
        )

        y += 35

        # Anotações
        y = self.render_text_section(
            screen,
            "Anotações do Mestre",
            self.faction.notes,
            y
        )

        self.content_height = (
            y - content_top + 20
        )

        screen.set_clip(previous_clip)

        self._clamp_scroll()
        
        self.message_dialog.render(screen)
        
        self.confirm_dialog.render(screen)

    def render_text_section(
        self,
        screen,
        heading,
        content,
        y
    ):
        title = self.name_font.render(
            heading,
            True,
            (230, 220, 245)
        )

        screen.blit(title, (80, y))
        y += 42

        lines = self.wrap_text(
            content or "Nenhuma informação registrada.",
            1000
        )

        for line in lines:
            line_surface = self.info_font.render(
                line,
                True,
                (175, 175, 190)
            )

            screen.blit(
                line_surface,
                (80, y)
            )

            y += 27

        return y

    def wrap_text(self, text, max_width):
        lines = []

        for paragraph in text.splitlines():
            if not paragraph.strip():
                lines.append("")
                continue

            current_line = ""

            for word in paragraph.split():
                candidate = (
                    f"{current_line} {word}".strip()
                )

                if (
                    self.info_font.size(candidate)[0]
                    <= max_width
                    or not current_line
                ):
                    current_line = candidate
                else:
                    lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

        return lines

    def _clamp_scroll(self):
        max_scroll = max(
            0,
            self.content_height
            - self.content_rect.height
        )

        self.scroll_offset = max(
            0,
            min(self.scroll_offset, max_scroll)
        )

    def handle_edit_form_events(self, event):
        action = self.faction_form.handle_event(
            event
        )    
        
        if action == "cancel":
            self.cancel_edit()
            return
        
        if action == "submit":
            self.update_faction()
            return
        
    def cancel_edit(self):
        self.faction_form.clear()
        
        self.view_mode = (
            WorldFactionViewMode.DETAILS
        )
        
    def update_faction(self):
        if (
            self.world.id is None
            or self.faction.id is None
        ):
            return
        
        updated_faction = (
            self.faction_form.build_faction(
                self.world.id
            )
        )
        
        if updated_faction is None:
            return
        
        # Preserva a identidade da facção
        updated_faction.id = self.faction.id
        
        self.app.faction_repository.update(
            updated_faction
        )
        
        # Recarrega os dados persistidos
        refreshed_faction = (
            self.app.faction_repository.get_by_id(
                self.faction.id
            )
        )
        
        if refreshed_faction is not None:
            self.faction = refreshed_faction
            
        self.faction_form.clear()
        
        self.scroll_offset = 0
        
        self.view_mode = (
            WorldFactionViewMode.DETAILS
        )

    def request_delete_faction(self):
        if self.faction.id is None:
            return
        
        self.confirm_dialog.open(
            "Excluir facção?",
            (
                f'Deseja excluir "{self.faction.name}"?'
            ),
            "Esta ação não pode ser desfeita",
            "Excluir"
        )

    def confirm_delete_faction(self):
        self.confirm_dialog.close()
        
        try:
            self.app.faction_repository.delete(
                self.faction
            )
        
        except (ValueError, sqlite3.Error) as error:
            self.message_dialog.set_message(
                "Não foi possível excluir",
                str(error)
            )
            
            self.message_dialog.open()
            return
        
        self.return_to_factions()
