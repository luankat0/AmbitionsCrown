import pygame

from src.ui.location.location_labels import (
    get_location_type_label
)

class LocationTreeView:
    def __init__(self):
        self.info_font = pygame.font.Font(
            None,
            24
        )
        
        self.indent_width = 28
        self.row_height = 38
        
        self.location_rects = []
        
    def _build_tree(
        self,
        locations
    ):
        locations_by_id = {}
        
        children_by_parent = {}
        
        for location in locations:
            if location.id is not None:
                locations_by_id[
                    location.id
                ] = location
                
        for location in locations:
            parent_id = (
                location.parent_location_id
            )
            
            if parent_id is None:
                continue
            
            children_by_parent.setdefault(
                parent_id,
                []
            ).append(
                location
            )
            
        roots = []
        
        for location in locations:
            parent_id = (
                location.parent_location_id
            )
            
            if parent_id is None:
                roots.append(
                    location
                )
                
        return roots, children_by_parent
    
    def render(
        self,
        screen,
        locations,
        start_x,
        start_y
    ):
        self.location_rects = []
        
        if not locations:
            empty_surface = (
                self.info_font.render(
                    "Nenhum local criado nesta região.",
                    True,
                    (150, 150, 160)
                )
            )
            
            screen.blit(
                empty_surface,
                (
                    start_x,
                    start_y
                )
            )
            
            return
        
        roots, children_by_parent = (
            self._build_tree(
                locations
            )
        )
        
        y = start_y
        
        visited = set()
        
        for root in roots:
            y = self._render_location(
                screen,
                root,
                children_by_parent,
                start_x,
                y,
                depth=0,
                visited=visited
            )
            
    def _render_location(
        self,
        screen,
        location,
        children_by_parent,
        start_x,
        y,
        depth,
        visited
    ):
        if location.id in visited:
            return y
        
        if location.id is not None:
            visited.add(
                location.id
            )
        
        x = (
            start_x
            + depth * self.indent_width
        )
        
        row_rect = pygame.Rect(
            x,
            y - 4,
            500 - (
                depth * self.indent_width
            ),
            self.row_height
        )
        
        self.location_rects.append(
            (
                location,
                row_rect
            )
        )
        
        marker = ""
        
        children = []
        
        if location.id is not None:
            children = (
                children_by_parent.get(
                    location.id,
                    []
                )
            )
        
        if children:
            marker = "• "
        
        name_text = (
            marker
            + location.name
        )
        
        name_surface = (
            self.info_font.render(
                name_text,
                True,
                (220, 220, 230)
            )
        )
        
        screen.blit(
            name_surface,
            (
                x,
                y
            )
        )
        
        type_text = (
            get_location_type_label(
                location.location_type
            )
        )
        
        type_surface = (
            self.info_font.render(
                type_text,
                True,
                (145, 145, 160)
            )
        )
        
        screen.blit(
            type_surface,
            (
                x + 260,
                y
            )
        )
        
        y += self.row_height
        
        for child in children:
            y = self._render_location(
                screen,
                child,
                children_by_parent,
                start_x,
                y,
                depth + 1,
                visited
            )
        
        return y

    def handle_event(
        self,
        event
    ):
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            for location, rect in (
                self.location_rects
            ):
                if rect.collidepoint(
                    event.pos
                ):
                    return location
        
        return None
    
    