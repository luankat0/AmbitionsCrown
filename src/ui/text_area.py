import pygame


class TextArea:
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
            24
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

        # Posição real do cursor na string.
        self.cursor_index = 0

        # Primeira linha visual exibida.
        self.scroll_line = 0

        self.scroll_speed = 2

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

                self.ensure_cursor_visible()

        # -------------------------
        # Scroll manual
        # -------------------------

        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(
                mouse_pos
            ):
                self.scroll_line -= (
                    event.y
                    * self.scroll_speed
                )

                self._clamp_scroll()

                return

        # -------------------------
        # Teclado
        # -------------------------

        if (
            event.type == pygame.KEYDOWN
            and self.active
        ):
            self.cursor_index = min(
                self.cursor_index,
                len(self.text)
            )

            if event.key == pygame.K_BACKSPACE:
                self._backspace()

            elif event.key == pygame.K_DELETE:
                self._delete()

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

            elif event.key == pygame.K_UP:
                self._move_cursor_vertical(-1)

            elif event.key == pygame.K_DOWN:
                self._move_cursor_vertical(1)

            elif event.key == pygame.K_HOME:
                self._move_cursor_home()

            elif event.key == pygame.K_END:
                self._move_cursor_end()

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_KP_ENTER
            ):
                self._insert_text("\n")

            elif event.key == pygame.K_TAB:
                return

            else:
                if event.unicode:
                    self._insert_text(
                        event.unicode
                    )

            self.ensure_cursor_visible()

    def render(self, screen):
        self.cursor_index = min(
            self.cursor_index,
            len(self.text)
        )

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
            self.scroll_line = 0

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

                    self.rect.y
                    + self.padding
                )
            )

            if self.active:
                lines = [
                    ("", 0, 0)
                ]

                self._render_cursor(
                    screen,
                    lines
                )

            return

        # -------------------------
        # Linhas visuais
        # -------------------------

        lines = self._build_visual_lines()

        self._clamp_scroll(
            lines
        )

        visible_count = (
            self._get_visible_line_count()
        )

        start_index = self.scroll_line

        end_index = min(
            len(lines),
            start_index
            + visible_count
        )

        previous_clip = screen.get_clip()

        content_rect = pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y + self.padding,
            self.rect.width
            - self.padding * 2,
            self.rect.height
            - self.padding * 2
        )

        screen.set_clip(
            content_rect
        )

        # -------------------------
        # Texto
        # -------------------------

        y = (
            self.rect.y
            + self.padding
        )

        line_height = (
            self.font.get_linesize()
        )

        for line_index in range(
            start_index,
            end_index
        ):
            line_text, _, _ = (
                lines[line_index]
            )

            surface = self.font.render(
                line_text,
                True,
                self.text_color
            )

            screen.blit(
                surface,
                (
                    self.rect.x
                    + self.padding,
                    y
                )
            )

            y += line_height

        # -------------------------
        # Cursor
        # -------------------------

        if self.active:
            self._render_cursor(
                screen,
                lines
            )

        screen.set_clip(
            previous_clip
        )

    def _insert_text(self, value):
        self.text = (
            self.text[
                :self.cursor_index
            ]
            + value
            + self.text[
                self.cursor_index:
            ]
        )

        self.cursor_index += len(
            value
        )

    def _backspace(self):
        if self.cursor_index <= 0:
            return

        self.text = (
            self.text[
                :self.cursor_index - 1
            ]
            + self.text[
                self.cursor_index:
            ]
        )

        self.cursor_index -= 1

    def _delete(self):
        if self.cursor_index >= len(
            self.text
        ):
            return

        self.text = (
            self.text[
                :self.cursor_index
            ]
            + self.text[
                self.cursor_index + 1:
            ]
        )

    def _build_visual_lines(self):
        max_width = (
            self.rect.width
            - self.padding * 2
        )

        if not self.text:
            return [
                ("", 0, 0)
            ]

        lines = []

        line_start = 0
        index = 0
        last_space = None

        while index < len(self.text):
            character = self.text[index]

            # Quebra explícita.
            if character == "\n":
                lines.append(
                    (
                        self.text[
                            line_start:index
                        ],
                        line_start,
                        index
                    )
                )

                index += 1
                line_start = index
                last_space = None

                continue

            candidate = self.text[
                line_start:index + 1
            ]

            width, _ = self.font.size(
                candidate
            )

            if width <= max_width:
                if character == " ":
                    last_space = index

                index += 1
                continue

            # -------------------------
            # Linha ultrapassou largura
            # -------------------------

            if (
                last_space is not None
                and last_space >= line_start
            ):
                break_index = (
                    last_space + 1
                )

                lines.append(
                    (
                        self.text[
                            line_start:break_index
                        ],
                        line_start,
                        break_index
                    )
                )

                line_start = break_index
                index = line_start
                last_space = None

                continue

            # Palavra maior que a caixa:
            # quebra no caractere.
            if index > line_start:
                lines.append(
                    (
                        self.text[
                            line_start:index
                        ],
                        line_start,
                        index
                    )
                )

                line_start = index
                last_space = None

                continue

            # Segurança para caracteres
            # excepcionalmente largos.
            lines.append(
                (
                    character,
                    index,
                    index + 1
                )
            )

            index += 1
            line_start = index
            last_space = None

        # Última linha.
        lines.append(
            (
                self.text[
                    line_start:
                ],
                line_start,
                len(self.text)
            )
        )

        return lines

    def _get_cursor_line_index(
        self,
        lines
    ):
        # Fazemos de trás para frente para
        # resolver corretamente linhas criadas
        # por quebra automática.
        for index in range(
            len(lines) - 1,
            -1,
            -1
        ):
            _, start, end = lines[index]

            if (
                start
                <= self.cursor_index
                <= end
            ):
                return index

        return 0

    def _move_cursor_vertical(
        self,
        direction
    ):
        lines = self._build_visual_lines()

        current_line_index = (
            self._get_cursor_line_index(
                lines
            )
        )

        target_line_index = max(
            0,
            min(
                current_line_index
                + direction,
                len(lines) - 1
            )
        )

        if (
            target_line_index
            == current_line_index
        ):
            return

        _, current_start, _ = (
            lines[current_line_index]
        )

        text_before_cursor = self.text[
            current_start:self.cursor_index
        ]

        desired_x, _ = self.font.size(
            text_before_cursor
        )

        _, target_start, target_end = (
            lines[target_line_index]
        )

        self.cursor_index = (
            self._find_nearest_index(
                target_start,
                target_end,
                desired_x
            )
        )

    def _find_nearest_index(
        self,
        start,
        end,
        target_x
    ):
        best_index = start
        best_distance = None

        for index in range(
            start,
            end + 1
        ):
            width, _ = self.font.size(
                self.text[
                    start:index
                ]
            )

            distance = abs(
                width - target_x
            )

            if (
                best_distance is None
                or distance < best_distance
            ):
                best_distance = distance
                best_index = index

        return best_index

    def _move_cursor_home(self):
        lines = self._build_visual_lines()

        line_index = (
            self._get_cursor_line_index(
                lines
            )
        )

        _, start, _ = lines[
            line_index
        ]

        self.cursor_index = start

    def _move_cursor_end(self):
        lines = self._build_visual_lines()

        line_index = (
            self._get_cursor_line_index(
                lines
            )
        )

        _, _, end = lines[
            line_index
        ]

        self.cursor_index = end

    def _get_visible_line_count(self):
        usable_height = (
            self.rect.height
            - self.padding * 2
        )

        line_height = (
            self.font.get_linesize()
        )

        return max(
            1,
            usable_height // line_height
        )

    def _clamp_scroll(
        self,
        lines=None
    ):
        if lines is None:
            lines = (
                self._build_visual_lines()
            )

        visible_count = (
            self._get_visible_line_count()
        )

        max_scroll = max(
            0,
            len(lines)
            - visible_count
        )

        self.scroll_line = max(
            0,
            min(
                self.scroll_line,
                max_scroll
            )
        )

    def ensure_cursor_visible(self):
        lines = self._build_visual_lines()

        cursor_line = (
            self._get_cursor_line_index(
                lines
            )
        )

        visible_count = (
            self._get_visible_line_count()
        )

        if cursor_line < self.scroll_line:
            self.scroll_line = cursor_line

        elif (
            cursor_line
            >= self.scroll_line
            + visible_count
        ):
            self.scroll_line = (
                cursor_line
                - visible_count
                + 1
            )

        self._clamp_scroll(
            lines
        )

    def _render_cursor(
        self,
        screen,
        lines
    ):
        # Cursor piscante.
        if (
            pygame.time.get_ticks()
            // 500
        ) % 2 != 0:
            return

        line_index = (
            self._get_cursor_line_index(
                lines
            )
        )

        visible_count = (
            self._get_visible_line_count()
        )

        if not (
            self.scroll_line
            <= line_index
            < self.scroll_line
            + visible_count
        ):
            return

        _, start, _ = lines[
            line_index
        ]

        text_before_cursor = self.text[
            start:self.cursor_index
        ]

        text_width, _ = self.font.size(
            text_before_cursor
        )

        line_height = (
            self.font.get_linesize()
        )

        visual_line = (
            line_index
            - self.scroll_line
        )

        cursor_x = (
            self.rect.x
            + self.padding
            + text_width
        )

        cursor_y = (
            self.rect.y
            + self.padding
            + visual_line
            * line_height
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
                + line_height - 2
            ),
            2
        )
        
    def _set_cursor_from_mouse(
        self,
        mouse_pos
    ):
        lines = self._build_visual_lines()
        
        if not lines:
            self.cursor_index = 0
            return
        
        line_height = (
            self.font.get_linesize()
        )
        
        mouse_y = (
            mouse_pos[1]
            - self.rect.y
            - self.padding
        )
        
        visual_line = max(
            0,
            mouse_y // line_height
        )
        
        line_index = (
            self.scroll_line
            + visual_line
        )
        
        line_index = max(
            0,
            min(
                line_index,
                len(lines) - 1
            )
        )
        
        _, start, end = lines[
            line_index
        ]
        
        mouse_x = (
            mouse_pos[0]
            - self.rect.x
            - self.padding
        )
        
        self.cursor_index = (
            self._find_nearest_index(
                start,
                end,
                mouse_x
            )
        )
        
    def clear(self):
        self.text = ""
        self.cursor_index = 0
        self.scroll_line = 0
        self.active = False
        
