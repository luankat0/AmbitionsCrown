import pygame

from enum import Enum, auto

from src.domain.campaign.models.campaign import CampaignStatus

from src.ui.button import Button
from src.ui.campaign.campaign_form import CampaignForm
from src.ui.campaign.campaign_setup_dialog import (
    CampaignSetupDialog,
)

class CampaignViewMode(Enum):
    LIST = auto()
    FORM = auto()

class CampaignScreen:
    def __init__(self, app):
        self.app = app
        
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.name_font = pygame.font.Font(
            None,
            30
        )
        
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.background_color = (
            30,
            30,
            35
        )
        
        self.campaigns = (
            self.app
            .campaign_repository
            .get_all()
        )
        
        self.view_mode = CampaignViewMode.LIST
        
        self.form = CampaignForm()
        
        self.setup_dialog = CampaignSetupDialog()
        
        self.setup_campaign = None
        self.setup_world = None
        
        self.new_campaign_button = Button(
            80,
            110,
            190,
            45,
            "+ Nova Campanha"
        )
        
        self.manage_worlds_button = Button(
            290,
            110,
            190,
            45,
            "Gerenciar Mundos"
        )
        
        self.card_rects = []
        
        self.scroll_offset = 0
        self.scroll_speed = 40
        
        self.list_rect = pygame.Rect(
            60,
            180,
            560,
            500
        )
        
    def handle_event(self, event):
        if self.setup_dialog.visible:
            self.handle_setup_dialog_event(
                event
            )
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.view_mode == CampaignViewMode.FORM:
                    self.cancel_form()
                    return
        
        if self.view_mode == CampaignViewMode.FORM:
            self.handle_form_events(event)
        else:
            self.handle_list_events(event)
    
    def handle_setup_dialog_event(
        self,
        event
    ):
        action, world = (
            self.setup_dialog.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.setup_dialog.close()
            
            self.setup_campaign = None
            self.setup_world = None
            
            return
        
        if (
            action == "confirm"
            and world is not None
        ):
            campaign = self.setup_campaign
            
            if campaign is None:
                return
            
            if campaign.world_id is None:
                campaign.world_id = world.id
                
                self.app.campaign_repository.update(
                    campaign
                )
            
            elif campaign.world_id != world.id:
                raise ValueError(
                    "Não é possível trocar o mundo "
                    "durante a inicialização da campanha."
                )
                
            self.app.campaign_snapshot_service.create_initial_snapshot(
                campaign
            )
            
            self.setup_world = world
            
            self.setup_dialog.close()
            
            self.setup_campaign = None
            self.setup_world = None
            
            self.app.select_campaign(
                campaign
            )
            
            self.app.change_screen(
                "dashboard"
            )
            
            return
    
    def handle_list_events(self, event):
        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.list_rect.collidepoint(
                mouse_pos
            ):
                self.scroll_offset -= (
                    event.y
                    * self.scroll_speed
                )
                
                self._clamp_scroll()
                
                return
        
        if self.new_campaign_button.handle_event(
            event
        ):
            self.form.prepare_create()
            
            self.view_mode = (
                CampaignViewMode.FORM
            )
            
            return
        
        if self.manage_worlds_button.handle_event(
            event
        ):
            self.app.change_screen(
                "world_library"
            )
            
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.list_rect.collidepoint(
                event.pos
            )
        ):
            for campaign, rect in self.card_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    self.open_campaign(
                        campaign
                    )
                    
                    return
                
    def handle_form_events(self, event):
        action = self.form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_form()
            return
        
        if action == "submit":
            self.create_campaign()
            return
       
    def update(self):
        pass
    
    def create_campaign(self):
        campaign = (
            self.form.build_campaign()
        )
        
        if campaign is None:
            return
        
        self.app.campaign_repository.add(
            campaign
        )
        
        self.campaigns.insert(
            0,
            campaign
        )
        
        self.scroll_offset = 0
        
        self.form.clear()
        
        self.view_mode = (
            CampaignViewMode.LIST
        )
    
    def render(self, screen):
        screen.fill(
            self.background_color
        )
        
        if self.view_mode == CampaignViewMode.FORM:
            self.form.render(
                screen
            )
            
        else:
            self.render_list(
                screen
            )
            
        if self.setup_dialog.visible:
            self.setup_dialog.render(
                screen
            )
    
    def render_list(self, screen):
        title = self.title_font.render(
            "Campanhas",
            True,
            (240, 240, 245)
        )
        
        self.new_campaign_button.render(
            screen
        )
        
        self.manage_worlds_button.render(
            screen
        )
        
        screen.blit(
            title,
            (80, 60)
        )
        
        self.card_rects = []
        
        if not self.campaigns:
            empty_text = (
                self.info_font.render(
                    "Nenhuma campanha criada.",
                    True,
                    (150, 150, 150)
                )
            )
            
            screen.blit(
                empty_text,
                (80, 190)
            )
            
            return
        
        y = (
            190
            - self.scroll_offset 
        )
        
        previous_clip = screen.get_clip()
        
        screen.set_clip(
            self.list_rect
        )
        
        for campaign in self.campaigns:
            card_rect = pygame.Rect(
                80,
                y,
                500,
                90
            )
            
            self.card_rects.append(
                (
                    campaign,
                    card_rect
                ),
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                card_rect,
                border_radius=8
            )
            
            name_surface = (
                self.name_font.render(
                    campaign.name,
                    True,
                    (235, 235, 240)
                )
            )
            
            screen.blit(
                name_surface,
                (
                    card_rect.x + 20,
                    card_rect.y + 15
                )
            )
            
            status_text = (
                self._get_status_label(
                    campaign.status
                )
            )
            
            status_surface = (
                self.info_font.render(
                    status_text,
                    True,
                    (160, 160, 175)
                )
            )
            
            screen.blit(
                status_surface,
                (
                    card_rect.x + 20,
                    card_rect.y + 52
                )
            )
            
            y += 110
            
        screen.set_clip(
            previous_clip
        )
            
    def _get_status_label(
        self,
        status: CampaignStatus
    ):
        labels = {
            CampaignStatus.PLANNING:
                "Planejamento",

            CampaignStatus.ACTIVE:
                "Ativa",

            CampaignStatus.PAUSED:
                "Pausada",

            CampaignStatus.FINISHED:
                "Finalizada",

            CampaignStatus.ARCHIVED:
                "Arquivada",
        }
        
        return labels.get(
            status,
            status.value
        )
        
    def cancel_form(self):
        self.form.clear()
        
        self.view_mode = (
            CampaignViewMode.LIST
        )

    def _clamp_scroll(self):
        if not self.campaigns:
            self.scroll_offset = 0
            return
        
        card_height = 90
        card_spacing = 20
        
        content_height = (
            len(self.campaigns)
            * (
                card_height
                + card_spacing
            )
            - card_spacing
        )
        
        max_scroll = max(
            0,
            content_height
            - self.list_rect.height
        )
        
        self.scroll_offset = max(
            0,
            min(
                self.scroll_offset,
                max_scroll
            )
        )

    def open_campaign(
        self,
        campaign
    ):
        if campaign.snapshot_created_at is not None:
            self.app.select_campaign(
                campaign
            )
            
            self.app.change_screen(
                "dashboard"
            )
            return
        
        worlds = (
            self.app
            .world_repository
            .get_all()
        )
        
        if campaign.world_id is not None:
            worlds = [
                world
                for world in worlds
                if world.id == campaign.world_id
            ]
        
        self.setup_campaign = campaign
        self.setup_world = None
        
        self.setup_dialog.open(
            campaign,
            worlds
        )

