import pygame


def draw_location_row(
    screen: pygame.Surface,
    font: pygame.font.Font,
    name: str,
    location_type_label: str,
    x: int,
    y: int,
    type_offset: int,
) -> None:
    name_surface = font.render(
        name,
        True,
        (220, 220, 230)
    )
    
    screen.blit(
        name_surface,
        (x, y)
    )
    
    type_surface = font.render(
        location_type_label,
        True,
        (145, 145, 160)
    )
    
    screen.blit(
        type_surface,
        (x + type_offset, y)
    )