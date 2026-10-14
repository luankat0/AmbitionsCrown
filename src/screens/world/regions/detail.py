import pygame

from enum import Enum, auto

from src.ui.button import Button
from src.ui.scroll import clamp_scroll

from src.ui.dialogs.confirm_dialog import ConfirmDialog
from src.ui.dialogs.message_dialog import MessageDialog

from src.ui.region.region_form import RegionForm
from src.ui.location.location_form import LocationForm


class WorldRegionViewMode(Enum):
    DETAILS = auto()
    LOCATION_FORM = auto()
    REGION_FORM = auto()


class WorldRegionScreen:
    def __init__(
        self,
        app,
        world,
        region
    ):
        self.app = app
        self.world = world
        self.region = region
        
        self.background_color = (
            30, 30, 35
        )
        
        self.title_font = pygame.font.Font(
            None, 48
        )
        
        self.name_font = pygame.font.Font(
            None, 32
        )
        
        self.info_font = pygame.font.Font(
            None, 24
        )
        
        self.back_button = Button(
            80, 110,
            220, 45,
            "← Voltar ao Mundo"
        )
        
        self.view_mode = WorldRegionViewMode.DETAILS
        
        self.location_form = LocationForm()
        
        self.new_location_button = Button(
            650,
            285,
            190,
            45,
            "+ Novo Local"
        )
        
        self.region_form = RegionForm()
        
        self.edit_region_button = Button(
            440, 285, 185, 45,
            "Editar Região"
        )
                
        self.delete_region_button = Button(
            860, 285, 190, 45,
            "Excluir Região"
        )
                
        self.confirm_dialog = ConfirmDialog()
                
        self.message_dialog = MessageDialog(
            "",
            ""
        )
        
        self.locations = []
        self.location_card_rects = []
        
        self.list_rect = pygame.Rect(
            80, 330, 850, 320
        )
        
        self.scroll_offset = 0
        self.scroll_speed = 40
        
        self.refresh_locations()
        
    def refresh_locations(self):
        if self.region.id is None:
            self.locations = []
            return
        
        locations = (
            self.app
            .location_repository
            .get_all_by_region(
                self.region.id
            )
        )
        
        self.locations = [
            location
            for location in locations
            if location.parent_location_id is None
        ]
        
    def handle_event(self, event):
        
        # Diálogos com Prioridade
        if self.message_dialog.visible:
            self.message_dialog.handle_event(
                event
            )
            return

        if self.confirm_dialog.visible:
            action = self.confirm_dialog.handle_event(
                event
            )
            
            if action == "cancel":
                self.confirm_dialog.close()
                
            if action == "confirm":
                self.confirm_delete_region()
                return
            
            return
        
        # Tratamento do ESC / Retorno
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == WorldRegionViewMode.REGION_FORM
            ):
                self.cancel_region_form()
                return
            
            if (
                self.view_mode
                == WorldRegionViewMode.LOCATION_FORM
            ):
                self.cancel_location_form()
                return
            
            self.return_to_world()
            return
        
        # Tratamento de Acesso aos FORMs
        if (
            self.view_mode
            == WorldRegionViewMode.REGION_FORM
        ):
            self.handle_region_form_events(event)
            return
        
        if (
            self.view_mode
            == WorldRegionViewMode.LOCATION_FORM
        ):
            self.handle_location_form_events(
                event
            )
            return
        
        # Botão Voltar
        if self.back_button.handle_event(event):
            self.return_to_world()
            return
        
        # Botão Editar Região
        if self.edit_region_button.handle_event(event):
            self.region_form.prepare_edit(
                self.region
            )
            
            self.view_mode = (
                WorldRegionViewMode.REGION_FORM
            )
            return
        
        # Botão Deletar Região
        if self.delete_region_button.handle_event(event):
            self.request_delete_region()
            return
            
        # Botão Criar Novo Local
        if self.new_location_button.handle_event(event):
            self.location_form.prepare_create()
            
            self.view_mode = (
                WorldRegionViewMode.LOCATION_FORM
            )
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.list_rect.collidepoint(event.pos):
                for location, rect in self.location_card_rects:
                    if rect.collidepoint(event.pos):
                        self.app.open_world_location(
                            self.world,
                            self.region,
                            location
                        )
                        return
        
        if event.type == pygame.MOUSEWHEEL:
            if self.list_rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.scroll_offset -= (
                    event.y * self.scroll_speed
                )
                
                self._clamp_scroll()
                
    def return_to_world(self):
        self.app.open_world_manager(
            self.world
        )
        
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill(
            self.background_color
        )
        
        if (
            self.view_mode
            == WorldRegionViewMode.REGION_FORM
        ):
            self.region_form.render(screen)
            return
        
        if (
            self.view_mode
            == WorldRegionViewMode.LOCATION_FORM
        ):
            self.location_form.render(screen)
            return
        
        title_surface = (
            self.title_font.render(
                "Gerenciar Região",
                True,
                (240, 240, 245)
            )
        )
        
        screen.blit(
            title_surface,
            (80, 55)
        )
        
        self.back_button.render(
            screen
        )
        
        self.edit_region_button.render(
            screen
        )
        
        self.delete_region_button.render(
            screen
        )
        
        self.new_location_button.render(
            screen
        )
        
        region_surface = (
            self.title_font.render(
                self.region.name,
                True,
                (230, 220, 245)
            )
        )
        
        screen.blit(
            region_surface,
            (80, 180)
        )
        
        description = (
            self.region.description
            or "Sem descrição."
        )
        
        description_surface = (
            self.info_font.render(
                description,
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            description_surface,
            (80, 235)
        )
        
        section_surface = (
            self.name_font.render(
                f"Locais ({len(self.locations)})",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            section_surface,
            (80, 290)
        )
        
        self.render_locations(
            screen
        )
        
        self.message_dialog.render(
            screen
        )

        self.confirm_dialog.render(
            screen
        )
        
    def render_locations(self, screen):
        self.location_card_rects = []
        
        if not self.locations:
            empty_surface = (
                self.info_font.render(
                    "Esta região não possui locais.",
                    True,
                    (160, 160, 175)
                )
            )
            
            screen.blit(
                empty_surface,
                (80, 345)
            )
            
            return
        
        self._clamp_scroll()
        
        previous_clip = screen.get_clip()
        
        screen.set_clip(
            self.list_rect
        )
        
        y = (
            self.list_rect.y
            + 10
            - self.scroll_offset
        )
        
        for location in self.locations:
            rect = pygame.Rect(
                80, y,
                760, 75
            )
            
            self.location_card_rects.append(
                (location, rect)
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                rect,
                border_radius=8
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
                (
                    rect.x + 20,
                    rect.y + 10
                )
            )
            
            description = (
                location.description
                or "Sem descrição."
            )
            
            description_surface = (
                self.info_font.render(
                    description,
                    True,
                    (155, 155, 165)
                )
            )
            
            screen.blit(
                description_surface,
                (
                    rect.x + 20,
                    rect.y + 45
                )
            )
            
            y += 90
        
        screen.set_clip(
            previous_clip
        )
        
    def _clamp_scroll(self):
        content_height = max(
            0,
            len(self.locations) * 90 - 5
        )
        
        self.scroll_offset = clamp_scroll(
            self.scroll_offset,
            content_height,
            self.list_rect.height
        )
        
    def handle_location_form_events(self, event):
        action = self.location_form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_location_form()
            return
        
        if action == "submit":
            self.create_location()
            return
        
    def cancel_location_form(self):
        self.location_form.clear()
        
        self.view_mode = (
            WorldRegionViewMode.DETAILS
        )
        
    def create_location(self):
        if self.region.id is None:
            return
        
        location = (
            self.location_form.build_location(
                region_id=self.region.id,
                parent_location_id=None
            )
        )
        
        if location is None:
            return
        
        self.app.location_repository.add(
            location
        )
        
        self.refresh_locations()
        
        self.scroll_offset = 0
        
        self.location_form.clear()
        
        self.view_mode = (
            WorldRegionViewMode.DETAILS
        )

    def handle_region_form_events(self, event):
        action = self.region_form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_region_form()
            return
        
        if action == "submit":
            self.update_region()
            return
        
    def cancel_region_form(self):
        self.region_form.clear()
        
        self.view_mode = (
            WorldRegionViewMode.DETAILS
        )
        
    def update_region(self):
        if (
            self.world.id is None
            or self.region.id is None
        ):
            return
        
        updated_region = (
            self.region_form.build_region(
                self.world.id
            )
        )
        
        if updated_region is None:
            return
        
        updated_region.id = self.region.id
        
        self.app.region_repository.update(
            updated_region
        )
        
        refreshed_region = (
            self.app
            .region_repository
            .get_by_id(
                self.region.id
            )
        )
        
        if refreshed_region is not None:
            self.region = refreshed_region
            
        self.region_form.clear()
        
        self.view_mode = (
            WorldRegionViewMode.DETAILS
        )

    def request_delete_region(self):
        if self.region.id is None:
            return
        
        locations = (
            self.app
            .location_repository
            .get_all_by_region(
                self.region.id
            )
        )
        
        if locations:
            location_count = len(locations)
            
            label = (
                "local"
                if location_count == 1
                else "locais"
            )
            
            self.message_dialog.set_message(
                "Não é possível excluir",
                (
                    f'Esta região possui '
                    f'{location_count} {label}'
                )
            )
            
            self.message_dialog.open()
            return
        
        self.confirm_dialog.open(
            "Excluir região?",
            (
                f'Deseja excluir "{self.region.name}"?'
            ),
            "Esta ação não pode ser desfeita.",
            "Excluir"
        )
    
    def confirm_delete_region(self):
        self.confirm_dialog.close()
        
        try:
            self.app.region_repository.delete(
                self.region
            )
            
        except ValueError as error:
            self.message_dialog.set_message(
                "Não é possível excluir",
                str(error)
            )
            self.message_dialog.open()
            return
        
        self.return_to_world()
