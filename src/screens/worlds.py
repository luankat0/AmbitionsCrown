import pygame

from enum import Enum, auto

from src.models.region import RegionType

from src.ui.button import Button
from src.ui.world.world_form import WorldForm

from src.screens.base_screen import BaseScreen

class WorldViewMode(Enum):
    CURRENT = auto()
    SELECT = auto()
    FORM = auto()

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
        
        self.region = []
        
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
            
        elif self.view_mode == WorldViewMode.SELECT:
            self.handle_selection_events(
                event
            )
            
        else:
            self.handle_current_events(
                event
            )
                
    def handle_current_events(self, event):            
        if self.change_world_button.handle_event(
            event
        ):
            self.view_mode = (
                WorldViewMode.SELECT
            )
            
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
        self.render_regions(
            screen
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
        
    def render_regions(
        self,
        screen
    ):
        section_title = (
            self.name_font.render(
                "Regiões",
                True,
                (235, 235, 240)
            )
        )
        
        screen.blit(
            section_title,
            (300, 290)
        )
        
        if not self.regions:
            empty_surface = (
                self.info_font.render(
                    "Nenhuma região criada neste mundo.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (300, 345)
            )
            
            return
        
        y = 345
        
        for region in self.regions:
            card_rect = pygame.Rect(
                300,
                y,
                600,
                75
            )
            
            pygame.draw.rect(
                screen,
                (45, 45, 55),
                card_rect,
                border_radius=8
            )
            
            name_surface = (
                self.info_font.render(
                    region.name,
                    True,
                    (235, 235, 240)
                )
            )
            
            screen.blit(
                name_surface,
                (
                    card_rect.x + 20,
                    card_rect.y + 12
                )
            )
            
            type_text = (
                self._get_region_type_label(
                    region.region_type
                )
            )
            
            type_surface = (
                self.info_font.render(
                    type_text,
                    True,
                    (155, 155, 165)
                )
            )
            
            screen.blit(
                type_surface,
                (
                    card_rect.x + 20,
                    card_rect.y + 42
                )
            )
            
            y += 90
            
    def _get_region_type_label(
        self,
        region_type: RegionType
    ):
        labels = {
            RegionType.KINGDOM:
            "Reino",

            RegionType.PROVINCE:
                "Província",

            RegionType.TERRITORY:
                "Território",

            RegionType.FOREST:
                "Floresta",

            RegionType.DESERT:
                "Deserto",

            RegionType.MOUNTAINS:
                "Montanhas",

            RegionType.ISLAND:
                "Ilha",

            RegionType.OTHER:
                "Outro",
        }
        
        return labels.get(
            region_type,
            region_type.value
        )

