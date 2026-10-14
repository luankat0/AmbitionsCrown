import pygame

from enum import Enum, auto

from src.ui.region.region_form import RegionForm
from src.ui.region.region_list_view import RegionListView

from src.screens.base_screen import BaseScreen

class WorldViewMode(Enum):
    CURRENT = auto()
    REGION_FORM = auto()

class WorldScreen(BaseScreen):
    def __init__(self, app):
        super().__init__(
            app,
            "world"
        )
                
        self.title_font = pygame.font.Font(
            None,
            48
        )
        
        self.name_font = pygame.font.Font(
            None,
            48
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
        
        self.worlds = (
            self.app
            .world_repository
            .get_all()
        )
        
        self.regions = []
        
        self.region_form = RegionForm()
        
        self.region_list_view = (
            RegionListView()
        )
        
        campaign = self.app.current_campaign

        if (
            campaign is not None
            and campaign.world_id is not None
        ):
            self.view_mode = (
                WorldViewMode.CURRENT
            )
            
        self.refresh_regions()
        
    def handle_event(self, event):
        super().handle_event(event)
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            if (
                self.view_mode
                == WorldViewMode.REGION_FORM
            ):
                self.cancel_region_form()
                return

        if (
            self.view_mode
            == WorldViewMode.REGION_FORM
        ):
            self.handle_region_form_events(
                event
            )
            return

        self.handle_world_current_events(
            event
        )
                
    def handle_world_current_events(
        self, 
        event
    ):            
        action, region = (
            self.region_list_view
            .handle_event(
                event
            )
        )
        
        if action == "new":
            self.region_form.prepare_create()
            
            self.view_mode = (
                WorldViewMode.REGION_FORM
            )
            
            return
        
        if (
            action == "select"
            and region is not None
        ):
            self.select_region(
                region
            )
            
            return
    
    def update(self):
        pass
    
    def render(self, screen):
        super().render(
            screen
        )
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
            
        if self.view_mode == WorldViewMode.REGION_FORM:
            self.region_form.render(
                screen
            )
            return
        
        self.render_current_world(
            screen
        )
            
    def render_current_world(
        self, 
        screen
    ):
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        if campaign.world_id is None:
            return
        
        world = (
            self.app
            .world_repository
            .get_by_id(
                campaign.world_id
            )
        )
        
        if world is None:
            missing_surface = (
                self.info_font.render(
                    "O mundo associado não foi encontrado.",
                    True,
                    (200, 90, 100)
                )
            )
            
            screen.blit(
                missing_surface,
                (300, 130)
            )
            
            return
        
        label_surface = (
            self.info_font.render(
                "Mundo da campanha",
                True,
                (160, 160, 175)
            )
        )
        
        screen.blit(
            label_surface,
            (300, 120)
        )
        
        name_surface = (
            self.name_font.render(
                world.name,
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            name_surface,
            (300, 155)
        )
        
        self.region_list_view.render(
            screen,
            self.regions
        )
           
    def refresh_regions(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.id is None
        ):
            self.regions = []
            return
        
        self.regions = (
            self.app
            .campaign_region_repository
            .get_all_by_campaign(
                campaign.id
            )
        )
                
    def handle_region_form_events(
        self,
        event
    ):
        action = (
            self.region_form.handle_event(
                event
            )
        )
        
        if action == "cancel":
            self.cancel_region_form()
            return
        
        if action == "submit":
            self.create_region()
            return
        
    def cancel_region_form(self):
        self.region_form.clear()
        
        self.view_mode = (
            WorldViewMode.CURRENT
        )
        
    def create_region(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.id is None
        ):
            return
        
        region = (
            self.region_form
            .build_campaign_region(
                campaign.id
            )
        )
        
        if region is None:
            return
        
        self.app.campaign_region_repository.add(
            region
        )
        
        self.regions.insert(
            0,
            region
        )
        
        self.region_form.clear()
        
        self.view_mode = (
            WorldViewMode.CURRENT
        )
        
    def select_region(
        self,
        region
    ):
        self.app.open_region(
            region
        )
        