import pygame

from src.ui.text_area import TextArea

class BaseForm:
    def __init__(self):
        self.fields = []
        self.validation_message = ""
        
    def clear(self):
        for field in self.fields:
            field.clear()
            
        self.validation_message = ""
        
    def prepare_create(self):
        self.clear()
        
        if self.fields:
            self._set_focus(0)
            
    def _set_focus(self, index):
        for field in self.fields:
            field.active = False
        
        active_field = self.fields[index]
        active_field.active = True
        
        if isinstance(
            active_field,
            TextArea
        ):
            active_field.ensure_cursor_visible()
            
    def _get_active_index(self):
        for index, field in enumerate(
            self.fields
        ):
            if field.active:
                return index
            
        return None
    
    def _move_focus(self, direction):
        current_index = (
            self._get_active_index()
        )
        
        if current_index is None:
            if direction > 0:
                next_index = 0
            else:
                next_index = (
                    len(self.fields) - 1
                )
                
        else:
            next_index = (
                current_index + direction
            ) % len(self.fields)
            
        self._set_focus(
            next_index
        )
        
    def handle_navigation_event(self, event):
        if event.type != pygame.KEYDOWN:
            return False, None
        
        if event.key == pygame.K_TAB:
            shift_pressed = bool(
                event.mod & pygame.KMOD_SHIFT
            )
            
            if shift_pressed:
                self._move_focus(-1)
            else:
                self._move_focus(1)
            
            return True, None
        
        if event.key in (
            pygame.K_RETURN,
            pygame.K_KP_ENTER
        ):
            shift_pressed = bool(
                event.mod & pygame.KMOD_SHIFT
            )
            
            active_index = (
                self._get_active_index()
            )
            
            active_field = None
            
            if active_index is not None:
                active_field = self.fields[
                    active_index
                ]
                
            if (
                shift_pressed
                and isinstance(
                    active_field,
                    TextArea
                )
            ):
                return False, None
            
            return True, "submit"
        
        return False, None
    
    def handle_fields_event(self, event):
        for field in self.fields:
            field.handle_event(event)