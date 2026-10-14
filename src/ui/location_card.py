import pygame


def draw_location_card(
    screen: pygame.Surface,
    rect: pygame.Rect,
    name: str,
    description: str | None,
    name_font: pygame.font.Font,
    info_font: pygame.font.Font
) -> None:
    pygame.draw.rect(
        screen,
        (45, 45, 55),
        rect,
        border_radius=8
    )
    
    name_surface = name_font.render(
        name,
        True,
        (235, 235, 240)
    )
    
    screen.blit(
        name_surface,
        (rect.x + 20, rect.y + 10)
    )
    
    description_surface = info_font.render(
        description or "Sem descrição.",
        True,
        (155, 155, 165)
    )
    
    screen.blit(
        description_surface,
        (rect.x + 20, rect.y + 45)
    )