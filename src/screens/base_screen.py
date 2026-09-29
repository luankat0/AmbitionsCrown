from src.ui.sidebar import Sidebar

class BaseScreen:
    def __init__(self, app, screen_name):
        self.app = app
        self.screen_name = screen_name

        self.background_color = (30, 30, 35)

        self.sidebar = Sidebar(
            app, screen_name
        )

    def handle_event(self, event):
        self.sidebar.handle_event(event)

    def update(self):
        pass

    def render(self, screen):
        screen.fill(self.background_color)

        self.sidebar.render(screen)