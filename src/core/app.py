import pygame

from src.core.database import Database

from src.repositories.npc_repository import NPCRepository

from src.screens.dashboard import DashboardScreen
from src.screens.npcs import NPCScreen

class App:
    def __init__(self):
        pygame.init()
        
        self.database = Database()
        self.database.create_tables()
        
        self.npc_repository = NPCRepository(
            self.database
        )

        self.width = 1280
        self.height = 720

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Ambitions Crown")

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_screen = DashboardScreen(self)

    def change_screen(self, screen_name):
            if screen_name == "dashboard":
                self.current_screen = DashboardScreen(self)
    
            elif screen_name == "npcs":
                self.current_screen = NPCScreen(self)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.current_screen.handle_event(event)

    def update(self):
        self.current_screen.update()

    def render(self):
        self.current_screen.render(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(60)

        self.database.close()
        
        pygame.quit()