import pygame

from enum import Enum, auto

from src.ui.button import Button

from src.ui.world.world_form import WorldForm
from src.ui.region.region_form import RegionForm

from src.ui.region.region_details_view import RegionDetailsView
from src.ui.region.region_list_view import RegionListView

from src.screens.base_screen import BaseScreen

class WorldViewMode(Enum):
    CURRENT = auto()
    SELECT = auto()
    FORM = auto()
    REGION_FORM = auto()
    REGION_DETAILS = auto()

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
        self.selected_region = None
        
        self.region_form = RegionForm()
        
        self.region_list_view = (
            RegionListView()
        )
        
        self.region_details_view = (
            RegionDetailsView()
        )
        
        self.form = WorldForm()
        
        self.new_world_button = Button(
            300,
            170,
            180,
            45,
            "+ Novo Mundo"
        )
        
        self.world_card_rects = []
        
        self.change_world_button = Button(
            300,
            200,
            180,
            45,
            "Trocar Mundo"
        )
        
        campaign = self.app.current_campaign

        if (
            campaign is not None
            and campaign.world_id is not None
        ):
            self.view_mode = (
                WorldViewMode.CURRENT
            )
        else:
            self.view_mode = (
                WorldViewMode.SELECT
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
            if self.view_mode == WorldViewMode.FORM:
                self.cancel_form()
                return
            
            if self.view_mode == WorldViewMode.REGION_FORM:
                self.cancel_region_form()
                return
            
            if self.view_mode == WorldViewMode.REGION_DETAILS:
                self.close_region()
                return
        
            if self.view_mode == WorldViewMode.SELECT:
                if campaign.world_id is not None:
                    self.view_mode = (
                        WorldViewMode.CURRENT
                    )
                    
                return
            
        if self.view_mode == WorldViewMode.FORM:
            self.handle_form_events(
                event
            )
            
        elif self.view_mode == WorldViewMode.REGION_FORM:
            self.handle_region_form_events(
                event
            )
            
        elif (
            self.view_mode
            == WorldViewMode.REGION_DETAILS
        ):
            self.handle_region_details_events(
                event
            )
            
        elif self.view_mode == WorldViewMode.SELECT:
            self.handle_selection_events(
                event
            )
            
        else:
            self.handle_current_events(
                event
            )
                
    def handle_current_events(
        self, 
        event
    ):            
        if self.change_world_button.handle_event(
            event
        ):
            self.view_mode = (
                WorldViewMode.SELECT
            )
            return
        
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
            
    def handle_selection_events(
        self,
        event
    ):
        if self.new_world_button.handle_event(
            event
        ):
            self.form.prepare_create()
            
            self.view_mode = (
                WorldViewMode.FORM
            )
            
            return
        
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for world, rect in (
                self.world_card_rects
            ):
                if rect.collidepoint(
                    event.pos
                ):
                    self.select_world(
                        world
                    )
                    
                    return
                
    def handle_form_events(
        self,
        event
    ):
        action = self.form.handle_event(
            event
        )
        
        if action == "cancel":
            self.cancel_form()
            return
        
        if action == "submit":
            self.create_world()
            return
        
    def cancel_form(self):
        self.form.clear()
        
        self.view_mode = (
            WorldViewMode.SELECT
        )
        
    def create_world(self):
        world = self.form.build_world()
        
        if world is None:
            return
        
        self.app.world_repository.add(
            world
        )
        
        self.worlds.insert(
            0,
            world
        )
        
        self.form.clear()
        
        self.select_world(
            world
        )
    
    def update(self):
        pass
    
    def render(self, screen):
        super().render(
            screen
        )
        
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        if self.view_mode == WorldViewMode.FORM:
            self.form.render(
                screen
            )
            
        elif self.view_mode == WorldViewMode.REGION_FORM:
            self.region_form.render(
                screen
            )
            
        elif (
            self.view_mode == WorldViewMode.REGION_DETAILS
        ):
            region = self.selected_region
            
            if region is not None:
                self.region_details_view.render(
                    screen,
                    region
                )
        
        elif self.view_mode == WorldViewMode.SELECT:
            self.render_world_selection(
                screen
            )
            
        else:
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
        
        self.change_world_button.render(
            screen
        )
        self.region_list_view.render(
            screen,
            self.regions
        )
        
    def render_world_selection(
        self,
        screen
    ):
        info_surface = (
            self.info_font.render(
                "Selecione um mundo para esta campanha:",
                True,
                (180, 180, 195)
            )
        )
        
        self.new_world_button.render(
            screen
        )
        
        screen.blit(
            info_surface,
            (300, 120)
        )
        
        self.world_card_rects = []
        
        if not self.worlds:
            empty_surface = (
                self.info_font.render(
                    "Nenhum mundo criado ainda.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (300, 240)
            )
            
            return
        
        y = 240
        
        for world in self.worlds:
            card_rect = pygame.Rect(
                300,
                y,
                600,
                90
            )
            
            self.world_card_rects.append(
                (
                    world,
                    card_rect
                )
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                card_rect,
                border_radius=8
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
                (
                    card_rect.x + 20,
                    card_rect.y + 15
                )
            )
            
            description = world.description
            
            if not description:
                description = (
                    "Sem descrição."
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
                    card_rect.x + 20,
                    card_rect.y + 52
                )
            )
            
            y += 110
            
    def select_world(
        self,
        world
    ):
        campaign = self.app.current_campaign
        
        if campaign is None:
            return
        
        campaign.world_id = world.id
        
        self.app.campaign_repository.update(
            campaign
        )
        
        self.refresh_regions()
        
        self.view_mode = (
            WorldViewMode.CURRENT
        )        
        
    def refresh_regions(self):
        campaign = self.app.current_campaign
        
        if (
            campaign is None
            or campaign.world_id is None
        ):
            self.regions = []
            return
        
        self.regions = (
            self.app
            .region_repository
            .get_all_by_world(
                campaign.world_id
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
            or campaign.world_id is None
        ):
            return
        
        region = (
            self.region_form.build_region(
                campaign.world_id
            )
        )
        
        if region is None:
            return
        
        self.app.region_repository.add(
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
        self.selected_region = region
        
        self.view_mode = (
            WorldViewMode.REGION_DETAILS
        )
        
    def handle_region_details_events(
        self,
        event
    ):
        action = (
            self.region_details_view
            .handle_event(
                event
            )
        )
        
        if action == "back":
            self.close_region()
            return
    
    def close_region(self):
        self.selected_region = None
        
        self.view_mode = (
            WorldViewMode.CURRENT
        )    
