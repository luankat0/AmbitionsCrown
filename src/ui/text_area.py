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

        # -------------------------
        # Scroll interno
        # -------------------------

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
                self.ensure_cursor_visible()

        # -------------------------
        # Scroll manual
        # -------------------------

        if event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_pos):
                self.scroll_line -= (
                    event.y
                    * self.scroll_speed
                )

                self._clamp_scroll()

                return

        # -------------------------
        # Digitação
        # -------------------------

        if (
            event.type == pygame.KEYDOWN
            and self.active
        ):
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            elif event.key == pygame.K_RETURN:
                self.text += "\n"

            elif event.key == pygame.K_TAB:
                return

            else:
                if event.unicode:
                    self.text += event.unicode

            self.ensure_cursor_visible()

    def render(self, screen):
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
        # Campo vazio
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
                self._render_cursor(
                    screen,
                    "",
                    0
                )

            return

        # -------------------------
        # Texto
        # -------------------------

        lines = self.wrap_text(
            self.text
        )

        self._clamp_scroll(
            lines
        )

        visible_line_count = (
            self._get_visible_line_count()
        )

        start_index = self.scroll_line

        end_index = min(
            len(lines),
            start_index
            + visible_line_count
        )

        visible_lines = lines[
            start_index:end_index
        ]

        line_height = (
            self.font.get_linesize()
        )

        y = (
            self.rect.y
            + self.padding
        )

        for line in visible_lines:
            text_surface = self.font.render(
                line,
                True,
                self.text_color
            )

            screen.blit(
                text_surface,
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
            cursor_line_index = (
                len(lines) - 1
            )

            if (
                start_index
                <= cursor_line_index
                < end_index
            ):
                visual_index = (
                    cursor_line_index
                    - start_index
                )

                self._render_cursor(
                    screen,
                    lines[cursor_line_index],
                    visual_index
                )

    def wrap_text(self, text):
        max_width = (
            self.rect.width
            - self.padding * 2
        )

        lines = []

        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            words = paragraph.split(" ")

            current_line = ""

            for word in words:
                test_line = current_line

                if test_line:
                    test_line += " "

                test_line += word

                width, _ = self.font.size(
                    test_line
                )

                if width <= max_width:
                    current_line = test_line

                else:
                    if current_line:
                        lines.append(
                            current_line
                        )

                    current_line = word

            lines.append(
                current_line
            )

        return lines

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
            if self.text:
                lines = self.wrap_text(
                    self.text
                )
            else:
                lines = [""]

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
        if self.text:
            lines = self.wrap_text(
                self.text
            )
        else:
            lines = [""]

        visible_count = (
            self._get_visible_line_count()
        )

        cursor_line = (
            len(lines) - 1
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
        line,
        visual_line_index
    ):
        # Faz o cursor piscar.
        if (
            pygame.time.get_ticks()
            // 500
        ) % 2 != 0:
            return

        text_width, _ = self.font.size(
            line
        )

        line_height = (
            self.font.get_linesize()
        )

        cursor_x = (
            self.rect.x
            + self.padding
            + text_width
        )

        cursor_y = (
            self.rect.y
            + self.padding
            + visual_line_index
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