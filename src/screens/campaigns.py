import pygame

from enum import Enum, auto

from src.models.campaign import CampaignStatus

from src.ui.button import Button
from src.ui.campaign.campaign_form import CampaignForm

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
        
        self.new_campaign_button = Button(
            80,
            110,
            190,
            45,
            "+ Nova Campanha"
        )
        
        self.card_rects = []
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.view_mode == CampaignViewMode.FORM:
                    self.cancel_form()
                    return
        
        if self.view_mode == CampaignViewMode.FORM:
            self.handle_form_events(event)
        else:
            self.handle_list_events(event)
    
    def handle_list_events(self, event):
        if self.new_campaign_button.handle_event(
            event
        ):
            self.form.prepare_create()
            
            self.view_mode = (
                CampaignViewMode.FORM
            )
            
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for campaign, rect in self.card_rects:
                if rect.collidepoint(
                    event.pos
                ):
                    self.app.select_campaign(
                        campaign
                    )
                    
                    self.app.change_screen(
                        "dashboard"
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
    
    def render_list(self, screen):
        title = self.title_font.render(
            "Campanhas",
            True,
            (240, 240, 245)
        )
        
        self.new_campaign_button.render(
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
        
        y = 190
        
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