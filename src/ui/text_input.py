import pygame


class TextInput:
    def __init__(
        self,
        x,
        y,
        width,
        height,
        placeholder=""
    ):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.text = ""
        self.placeholder = placeholder

        self.active = False

        self.font = pygame.font.Font(
            None,
            26
        )

        self.background_color = (
            40,
            40,
            48
        )

        self.border_color = (
            80,
            80,
            95
        )

        self.active_border_color = (
            120,
            120,
            160
        )

        self.text_color = (
            235,
            235,
            240
        )

        self.placeholder_color = (
            130,
            130,
            140
        )

        self.padding = 10

        # Posição do cursor dentro da string.
        self.cursor_index = 0

        # Deslocamento horizontal do texto.
        self.scroll_x = 0

    def handle_event(self, event):
        # -------------------------
        # Clique / foco
        # -------------------------

        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            self.active = self.rect.collidepoint(
                event.pos
            )

            if self.active:
                self._set_cursor_from_mouse(
                    event.pos
                )

                self._ensure_cursor_visible()

        # -------------------------
        # Teclado
        # -------------------------

        if (
            event.type == pygame.KEYDOWN
            and self.active
        ):
            # Garante que o cursor nunca fique
            # além do tamanho atual do texto.
            self.cursor_index = min(
                self.cursor_index,
                len(self.text)
            )

            if event.key == pygame.K_BACKSPACE:
                if self.cursor_index > 0:
                    self.text = (
                        self.text[
                            :self.cursor_index - 1
                        ]
                        + self.text[
                            self.cursor_index:
                        ]
                    )

                    self.cursor_index -= 1

            elif event.key == pygame.K_DELETE:
                if self.cursor_index < len(
                    self.text
                ):
                    self.text = (
                        self.text[
                            :self.cursor_index
                        ]
                        + self.text[
                            self.cursor_index + 1:
                        ]
                    )

            elif event.key == pygame.K_LEFT:
                self.cursor_index = max(
                    0,
                    self.cursor_index - 1
                )

            elif event.key == pygame.K_RIGHT:
                self.cursor_index = min(
                    len(self.text),
                    self.cursor_index + 1
                )

            elif event.key == pygame.K_HOME:
                self.cursor_index = 0

            elif event.key == pygame.K_END:
                self.cursor_index = len(
                    self.text
                )

            elif event.key == pygame.K_TAB:
                return

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            ):
                return

            else:
                if event.unicode:
                    self.text = (
                        self.text[
                            :self.cursor_index
                        ]
                        + event.unicode
                        + self.text[
                            self.cursor_index:
                        ]
                    )

                    self.cursor_index += len(
                        event.unicode
                    )

            self._ensure_cursor_visible()

    def render(self, screen):
        # Garante consistência quando outro
        # componente altera self.text diretamente.
        self.cursor_index = min(
            self.cursor_index,
            len(self.text)
        )

        self._ensure_cursor_visible()

        # -------------------------
        # Fundo
        # -------------------------

        pygame.draw.rect(
            screen,
            self.background_color,
            self.rect,
            border_radius=5
        )

        # -------------------------
        # Borda
        # -------------------------

        if self.active:
            border_color = (
                self.active_border_color
            )
        else:
            border_color = (
                self.border_color
            )

        pygame.draw.rect(
            screen,
            border_color,
            self.rect,
            width=2,
            border_radius=5
        )

        # -------------------------
        # Placeholder
        # -------------------------

        if not self.text:
            placeholder_surface = (
                self.font.render(
                    self.placeholder,
                    True,
                    self.placeholder_color
                )
            )

            screen.blit(
                placeholder_surface,
                (
                    self.rect.x
                    + self.padding,

                    self.rect.centery
                    - placeholder_surface
                    .get_height() // 2
                )
            )

            if self.active:
                self._render_cursor(
                    screen
                )

            return

        # -------------------------
        # Recorte interno
        # -------------------------

        previous_clip = screen.get_clip()

        content_rect = pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y,
            self.rect.width
            - self.padding * 2,
            self.rect.height
        )

        screen.set_clip(
            content_rect
        )

        # -------------------------
        # Texto
        # -------------------------

        text_surface = self.font.render(
            self.text,
            True,
            self.text_color
        )

        text_x = (
            self.rect.x
            + self.padding
            - self.scroll_x
        )

        text_y = (
            self.rect.centery
            - text_surface.get_height() // 2
        )

        screen.blit(
            text_surface,
            (
                text_x,
                text_y
            )
        )

        # -------------------------
        # Cursor
        # -------------------------

        if self.active:
            self._render_cursor(
                screen
            )

        screen.set_clip(
            previous_clip
        )

    def _ensure_cursor_visible(self):
        text_before_cursor = self.text[
            :self.cursor_index
        ]

        cursor_width, _ = self.font.size(
            text_before_cursor
        )

        visible_width = (
            self.rect.width
            - self.padding * 2
        )

        # Cursor passou da borda direita.
        if (
            cursor_width - self.scroll_x
            > visible_width
        ):
            self.scroll_x = (
                cursor_width
                - visible_width
            )

        # Cursor passou da borda esquerda.
        elif (
            cursor_width - self.scroll_x
            < 0
        ):
            self.scroll_x = cursor_width

        # Nunca permitimos scroll negativo.
        self.scroll_x = max(
            0,
            self.scroll_x
        )

        # Se todo o texto cabe novamente,
        # não há necessidade de scroll.
        total_width, _ = self.font.size(
            self.text
        )

        if total_width <= visible_width:
            self.scroll_x = 0

    def _render_cursor(self, screen):
        # Pisca a cada 500 ms.
        if (
            pygame.time.get_ticks()
            // 500
        ) % 2 != 0:
            return

        text_before_cursor = self.text[
            :self.cursor_index
        ]

        cursor_width, _ = self.font.size(
            text_before_cursor
        )

        cursor_x = (
            self.rect.x
            + self.padding
            + cursor_width
            - self.scroll_x
        )

        line_height = (
            self.font.get_linesize()
        )

        cursor_y = (
            self.rect.centery
            - line_height // 2
        )

        pygame.draw.line(
            screen,
            self.text_color,
            (
                cursor_x,
                cursor_y
            ),
            (
                cursor_x,
                cursor_y
                + line_height
            ),
            2
        )
        
    def _set_cursor_from_mouse(
        self,
        mouse_pos
    ):
        mouse_x = (
            mouse_pos[0]
            - self.rect.x
            - self.padding
            - self.scroll_x
        )
        
        best_index = 0
        best_distance = None
        
        for index in range(
            len(self.text) + 1
        ):
            width, _ = self.font.size(
                self.text[:index]
            )
            
            distance = abs(
                width - mouse_x
            )

            if (
                best_distance is None
                or distance < best_distance
            ):
                best_distance = distance
                best_index = index
        self.cursor_index = best_index