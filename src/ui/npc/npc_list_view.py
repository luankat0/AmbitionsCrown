import pygame

from src.models.npc import NPC

from src.ui.button import Button
from src.ui.text_input import TextInput

class NPCListView:
    def __init__(self):
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

        # Área visível da lista
        self.list_rect = pygame.Rect(
            280,
            190,
            900,
            450
        )

        # Configuração dos cards
        self.card_height = 65
        self.card_spacing = 15
        self.content_padding = 30

        # Scroll
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_speed = 40
        
        self.search_input = TextInput(
            460,
            110,
            360,
            45,
            "Buscar NPC..."
        )
        
        self.hovered_npc_id = None

    def handle_event(
        self,
        event,
        npcs: list[NPC]
    ):
        old_query = self.search_input.text
        
        self.search_input.handle_event(event)
        
        if self.search_input.text != old_query:
            self.scroll_offset = 0
            
        if self.new_npc_button.handle_event(event):
            return "create", None
        
        filtered_npcs = self._filter_npcs(
            npcs
        )
        
        if event.type == pygame.MOUSEMOTION:
            self.hovered_npc_id = None
            
            if self.list_rect.collidepoint(
                event.pos
            ):
                for index, npc in enumerate(
                    filtered_npcs
                ):
                    card_rect = self._get_card_rect(
                        index
                    )
                    
                    if card_rect.collidepoint(
                        event.pos
                    ):
                        self.hovered_npc_id = npc.id
                        break

        self._update_scroll_limits(
            filtered_npcs
        )

        # -------------------------
        # Scroll com roda do mouse
        # -------------------------

        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()

            if self.list_rect.collidepoint(
                mouse_pos
            ):
                self.scroll_offset -= (
                    event.y * self.scroll_speed
                )

                self._clamp_scroll()

            return None, None

        # -------------------------
        # Seleção de NPC
        # -------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                # Só selecionamos cards dentro
                # da área da lista.
                if not self.list_rect.collidepoint(
                    event.pos
                ):
                    return None, None

                for index, npc in enumerate(
                    filtered_npcs
                ):
                    card_rect = self._get_card_rect(
                        index
                    )

                    if card_rect.collidepoint(
                        event.pos
                    ):
                        return "select", npc

        return None, None

    def render(
        self,
        screen,
        npcs: list[NPC]
    ):
        filtered_npcs = self._filter_npcs(
            npcs
        )
        
        self._update_scroll_limits(
            filtered_npcs
        )

        # -------------------------
        # Título
        # -------------------------

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
        self.search_input.render(screen)
        
        result_count = len(filtered_npcs)
        
        if self.search_input.text.strip():
            count_text = (
                f"{result_count} resultado"
                if result_count == 1
                else f"{result_count} resultados"
            )
        else:
            count_text = (
                f"{result_count} NPC"
                if result_count == 1
                else f"{result_count} NPCs"
            )
        
        count_surface = self.info_font.render(
            count_text,
            True,
            (150, 150, 160)
        )
        
        screen.blit(
            count_surface,
            (850, 122)
        )

        # -------------------------
        # Fundo da lista
        # -------------------------

        pygame.draw.rect(
            screen,
            (36, 36, 44),
            self.list_rect,
            border_radius=8
        )

        if not filtered_npcs:
            if self.search_input.text.strip():
                message = (
                    "Nenhum NPC corresponde à busca."
                )
            else:
                message = (
                    "Nenhum NPC criado ainda."
                )
                
            empty_text = self.info_font.render(
                message,
                True,
                (150, 150, 160)
            )

            screen.blit(
                empty_text,
                (
                    self.list_rect.x + 30,
                    self.list_rect.y + 30
                )
            )

            return

        # -------------------------
        # Recorte da área da lista
        # -------------------------

        previous_clip = screen.get_clip()

        screen.set_clip(
            self.list_rect
        )

        # -------------------------
        # Cards
        # -------------------------

        for index, npc in enumerate(
            filtered_npcs
        ):
            card_rect = self._get_card_rect(
                index
            )

            # Não precisamos desenhar cards
            # completamente fora da tela.
            if not card_rect.colliderect(
                self.list_rect
            ):
                continue

            if npc.id == self.hovered_npc_id:
                card_color = (
                    58, 
                    58, 
                    72
                )
            else:
                card_color = (
                    45,
                    45,
                    55
                )
            
            pygame.draw.rect(
                screen,
                card_color,
                card_rect,
                border_radius=6
            )

            name_surface = (
                self.info_font.render(
                    npc.name,
                    True,
                    (235, 235, 240)
                )
            )

            screen.blit(
                name_surface,
                (
                    card_rect.x + 15,
                    card_rect.y + 10
                )
            )

            details_surface = (
                self.info_font.render(
                    npc.get_summary(),
                    True,
                    (155, 155, 165)
                )
            )

            screen.blit(
                details_surface,
                (
                    card_rect.x + 15,
                    card_rect.y + 35
                )
            )

        # Restauramos o recorte anterior.
        screen.set_clip(
            previous_clip
        )

        # -------------------------
        # Barra de scroll
        # -------------------------

        self._render_scrollbar(
            screen
        )

    def _get_card_rect(
        self,
        index: int
    ):
        card_step = (
            self.card_height
            + self.card_spacing
        )

        y = (
            self.list_rect.y
            + self.content_padding
            + index * card_step
            - self.scroll_offset
        )

        return pygame.Rect(
            self.list_rect.x + 20,
            y,
            self.list_rect.width - 60,
            self.card_height
        )

    def _update_scroll_limits(
        self,
        npcs: list[NPC]
    ):
        if not npcs:
            self.max_scroll = 0
            self.scroll_offset = 0
            return

        card_step = (
            self.card_height
            + self.card_spacing
        )

        content_height = (
            self.content_padding
            + (len(npcs) - 1) * card_step
            + self.card_height
            + self.content_padding
        )

        self.max_scroll = max(
            0,
            content_height
            - self.list_rect.height
        )

        self._clamp_scroll()

    def _clamp_scroll(self):
        self.scroll_offset = max(
            0,
            min(
                self.scroll_offset,
                self.max_scroll
            )
        )

    def _render_scrollbar(
        self,
        screen
    ):
        if self.max_scroll <= 0:
            return

        track_rect = pygame.Rect(
            self.list_rect.right - 12,
            self.list_rect.top + 10,
            5,
            self.list_rect.height - 20
        )

        pygame.draw.rect(
            screen,
            (65, 65, 75),
            track_rect,
            border_radius=3
        )

        total_height = (
            self.list_rect.height
            + self.max_scroll
        )

        visible_ratio = (
            self.list_rect.height
            / total_height
        )

        thumb_height = max(
            30,
            int(
                track_rect.height
                * visible_ratio
            )
        )

        available_movement = (
            track_rect.height
            - thumb_height
        )

        scroll_ratio = (
            self.scroll_offset
            / self.max_scroll
        )

        thumb_y = (
            track_rect.y
            + int(
                available_movement
                * scroll_ratio
            )
        )

        thumb_rect = pygame.Rect(
            track_rect.x,
            thumb_y,
            track_rect.width,
            thumb_height
        )

        pygame.draw.rect(
            screen,
            (135, 135, 150),
            thumb_rect,
            border_radius=3
        )

    def scroll_to_top(self):
        self.scroll_offset = 0
        
    def _filter_npcs(
        self,
        npcs: list[NPC]
    ):
        query = self.search_input.text.strip().casefold()
        
        if not query:
            return npcs
        
        filtered_npcs: list[NPC] = []
        
        for npc in npcs:
            searchable_text = " ".join([
                npc.name,
                npc.race,
                npc.role,
                npc.region
            ]).casefold()
            
            if query in searchable_text:
                filtered_npcs.append(npc)
        
        return filtered_npcs