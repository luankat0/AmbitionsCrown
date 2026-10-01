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