import pygame

from src.models.campaign import CampaignStatus

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
        
        self.card_rects = []
        
    def handle_event(self, event):
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
                
    def update(self):
        pass
    
    def render(self, screen):
        screen.fill(
            self.background_color
        )
        
        title = self.title_font.render(
            "Campanhas",
            True,
            (240, 240, 245)
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
                (80, 140)
            )
            
            return
        
        y = 140
        
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