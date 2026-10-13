import pygame

from src.ui.button import Button

from src.ui.faction.faction_labels import (
    get_faction_type_label,
    get_faction_status_label,
)


class WorldFactionScreen:
    def __init__(self, app, world, faction):
        self.app = app
        self.world = world
        self.faction = faction

        self.background_color = (30, 30, 35)

        self.title_font = pygame.font.Font(None, 48)
        self.name_font = pygame.font.Font(None, 34)
        self.info_font = pygame.font.Font(None, 24)

        self.back_button = Button(
            80, 110,
            220, 45,
            "Voltar às Facções"
        )

        self.content_rect = pygame.Rect(
            80, 175, 1080, 485
        )

        self.scroll_offset = 0
        self.scroll_speed = 40
        self.content_height = 0

    def handle_event(self, event):
        if (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            self.return_to_factions()
            return

        if self.back_button.handle_event(event):
            self.return_to_factions()
            return

        if event.type == pygame.MOUSEWHEEL:
            if self.content_rect.collidepoint(
                pygame.mouse.get_pos()
            ):
                self.scroll_offset -= (
                    event.y * self.scroll_speed
                )

                self._clamp_scroll()

    def return_to_factions(self):
        self.app.open_world_factions(
            self.world
        )

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.background_color)

        title = self.title_font.render(
            "Detalhes da Facção",
            True,
            (240, 240, 245)
        )

        screen.blit(title, (80, 55))

        self.back_button.render(screen)

        previous_clip = screen.get_clip()
        screen.set_clip(self.content_rect)

        content_top = (
            self.content_rect.y
            + 10
            - self.scroll_offset
        )

        y = content_top

        # Mundo ao qual a facção pertence
        world_text = self.info_font.render(
            f"Mundo: {self.world.name}",
            True,
            (165, 150, 185)
        )

        screen.blit(world_text, (80, y))
        y += 45

        # Nome da facção
        name = self.title_font.render(
            self.faction.name,
            True,
            (230, 220, 245)
        )

        screen.blit(name, (80, y))
        y += 70

        # Tipo
        faction_type = get_faction_type_label(
            self.faction.faction_type
        )

        type_text = self.info_font.render(
            f"Tipo: {faction_type}",
            True,
            (210, 210, 220)
        )

        screen.blit(type_text, (80, y))
        y += 35

        # Status
        faction_status = get_faction_status_label(
            self.faction.status
        )

        status_text = self.info_font.render(
            f"Status: {faction_status}",
            True,
            (210, 210, 220)
        )

        screen.blit(status_text, (80, y))
        y += 65

        # Descrição
        y = self.render_text_section(
            screen,
            "Descrição",
            self.faction.description,
            y
        )

        y += 35

        # Anotações
        y = self.render_text_section(
            screen,
            "Anotações do Mestre",
            self.faction.notes,
            y
        )

        self.content_height = (
            y - content_top + 20
        )

        screen.set_clip(previous_clip)

        self._clamp_scroll()

    def render_text_section(
        self,
        screen,
        heading,
        content,
        y
    ):
        title = self.name_font.render(
            heading,
            True,
            (230, 220, 245)
        )

        screen.blit(title, (80, y))
        y += 42

        lines = self.wrap_text(
            content or "Nenhuma informação registrada.",
            1000
        )

        for line in lines:
            line_surface = self.info_font.render(
                line,
                True,
                (175, 175, 190)
            )

            screen.blit(
                line_surface,
                (80, y)
            )

            y += 27

        return y

    def wrap_text(self, text, max_width):
        lines = []

        for paragraph in text.splitlines():
            if not paragraph.strip():
                lines.append("")
                continue

            current_line = ""

            for word in paragraph.split():
                candidate = (
                    f"{current_line} {word}".strip()
                )

                if (
                    self.info_font.size(candidate)[0]
                    <= max_width
                    or not current_line
                ):
                    current_line = candidate
                else:
                    lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

        return lines

    def _clamp_scroll(self):
        max_scroll = max(
            0,
            self.content_height
            - self.content_rect.height
        )

        self.scroll_offset = max(
            0,
            min(self.scroll_offset, max_scroll)
        )

