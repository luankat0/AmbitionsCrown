import pygame

from src.ui.button import Button
from src.ui.dialogs.base_dialog import BaseDialog


class CampaignSetupDialog(BaseDialog):
    def __init__(self):
        super().__init__(
            "Configurar Campanha",
            width=620,
            height=500
        )
        
        self.campaign = None
        self.worlds = []
        
        self.selected_world_index = None
        self.scroll_index = 0
        
        self.visible_world_count = 5
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.world_font = pygame.font.Font(
            None,
            26
        )
        
        self.cancel_button = Button(
            0,
            0,
            140,
            45,
            "Cancelar"
        )
        
        self.confirm_button = Button(
            0,
            0,
            180,
            45,
            "Iniciar Campanha"
        )
        
        self.world_rects = []
        
        self.error_message = ""
        
    @property
    def selected_world(self):
        if self.selected_world_index is None:
            return None
        
        if not (
            0
            <= self.selected_world_index
            < len(self.worlds)
        ):
            return None
        
        return self.worlds[
            self.selected_world_index
        ]
        
    def open(
        self,
        campaign,
        worlds
    ):
        self.campaign = campaign
        self.worlds = list(worlds)
        
        self.scroll_index = 0
        self.selected_world_index = None
        self.error_message = ""
        
        if self.worlds:
            self.selected_world_index = 0
            
        if (
            campaign.world_id is not None
            and self.worlds
        ):
            for index, world in enumerate(
                self.worlds
            ):
                if world.id == campaign.world_id:
                    self.selected_world_index = index
                    self._ensure_selected_visible()
                    break
        
        self.visible = True
        
    def close(self):
        super().close()
        
        self.campaign = None
        self.worlds = []
        self.selected_world_index = None
        self.scroll_index = 0
        self.world_rects = []
        
        self.error_message = ""
    
    def show_error(
        self,
        message
    ):
        self.error_message = message 

    def handle_event(
        self,
        event
    ):
        if not self.visible:
            return None, None
        
        if self.handle_base_event(
            event
        ):
            return "cancel", None
        
        if event.type == pygame.MOUSEWHEEL:
            if self.worlds:
                self.scroll_index -= event.y
                self._clamp_scroll()
                
            return None, None
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for index, rect in self.world_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    self.selected_world_index = index
                    self.error_message = ""
                    
                    return None, None
        
        if self.cancel_button.handle_event(
            event
        ):
            return "cancel", None
        
        if self.confirm_button.handle_event(
            event
        ):
            world = self.selected_world
            
            if world is not None:
                return "confirm", world
        
        return None, None
    
    def render(
        self,
        screen
    ):
        if not self.visible:
            return
        
        dialog_rect = self.render_base(
            screen
        )
        
        if dialog_rect is None:
            return
        
        if self.campaign is None:
            return
        
        campaign_surface = (
            self.info_font.render(
                f"Campanha: {self.campaign.name}",
                True,
                (220, 220, 230)
            )
        )
        
        screen.blit(
            campaign_surface,
            (
                dialog_rect.x + 40,
                dialog_rect.y + 75
            )
        )
        
        instruction_surface = (
            self.info_font.render(
                "Escolha o mundo base da campanha:",
                True,
                (170, 170, 185)
            )
        )
        
        screen.blit(
            instruction_surface,
            (
                dialog_rect.x + 40,
                dialog_rect.y + 115
            )
        )
        
        self.world_rects = []
        
        if not self.worlds:
            empty_surface = (
                self.info_font.render(
                    "Nenhum mundo disponível.",
                    True,
                    (180, 120, 120)
                )
            )
            
            screen.blit(
                empty_surface,
                (
                    dialog_rect.x + 40,
                    dialog_rect.y + 175
                )
            )
            
        else:
            self._render_worlds(
                screen,
                dialog_rect
            )
            
        explanation_surface = (
            self.info_font.render(
                (
                    "Será criado um estado independente "
                    "do mundo para esta campanha."
                ),
                True,
                (150, 150, 165)
            )
        )
        
        screen.blit(
            explanation_surface,
            (
                dialog_rect.x + 40,
                dialog_rect.bottom - 110
            )
        )
        
        self.cancel_button.rect.topleft = (
            dialog_rect.x + 150,
            dialog_rect.bottom - 65
        )
        
        self.confirm_button.rect.topleft = (
            dialog_rect.x + 310,
            dialog_rect.bottom - 65
        )
        
        self.cancel_button.render(
            screen
        )
        
        self.confirm_button.render(
            screen
        )
    
    def _render_worlds(
        self,
        screen,
        dialog_rect
    ):
        start = self.scroll_index
        
        end = min(
            len(self.worlds),
            start + self.visible_world_count
        )
        y = dialog_rect.y + 155
        
        for index in range(
            start,
            end
        ):
            world = self.worlds[index]
            
            rect = pygame.Rect(
                dialog_rect.x + 40,
                y,
                dialog_rect.width - 80,
                44
            )
            
            self.world_rects.append(
                (
                    index,
                    rect
                )
            )
            
            if index == self.selected_world_index:
                pygame.draw.rect(
                    screen,
                    (65, 65, 85),
                    rect,
                    border_radius=6
                ) 
            else:
                pygame.draw.rect(
                    screen,
                    (42, 42, 50),
                    rect,
                    border_radius=6
                )
            
            world_surface = (
                self.world_font.render(
                    world.name,
                    True,
                    (230, 230, 235)
                )
            )
            
            screen.blit(
                world_surface,
                (
                    rect.x + 15,
                    rect.centery
                    - world_surface.get_height() // 2
                )
            )
            
            y += 50
            
    def _clamp_scroll(self):
        max_scroll = max(
            0,
            len(self.worlds)
            - self.visible_world_count
        )
        
        self.scroll_index = max(
            0,
            min(
                self.scroll_index,
                max_scroll
            )
        )
    
    def _ensure_selected_visible(self):
        if self.selected_world_index is None:
            return
        
        if (
            self.selected_world_index
            < self.scroll_index
        ):
            self.scroll_index = (
                self.selected_world_index
            )
        
        elif (
            self.selected_world_index
            >= self.scroll_index
            + self.visible_world_count
        ):
            self.scroll_index = (
                self.selected_world_index
                - self.visible_world_count
                + 1
            )
            
        self._clamp_scroll()

