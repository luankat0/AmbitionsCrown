import pygame

from src.screens.base_screen import BaseScreen
from src.ui.button import Button

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

        self.new_npc_button = Button(
            280,
            110,
            160,
            45,
            "+ Novo NPC"
        )

    def handle_event(self, event):
        super().handle_event(event)

        if self.new_npc_button.handle_event(event):
            print("Botão Novo NPC clicado!") # Remover dps

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.change_screen("dashboard")

    def render(self, screen):
        super().render(screen)

        title = self.title_font.render(
            "NPCs",
            True,
            (240, 240, 240)
        )

        screen.blit(
            title,
            (280, 40)
        )

        self.new_npc_button.render(screen)

        # Área da lista dos NPCs
        list_rect = pygame.Rect(
            280,
            190,
            900,
            450
        )

        pygame.draw.rect(
            screen,
            (36, 36, 44),
            list_rect,
            border_radius=8
        )

        empty_text = self.info_font.render(
            "Nenhum NPC criado ainda.",
            True,
            (150, 150, 160)
        )

        screen.blit(
            empty_text,
            (310, 220)
        )