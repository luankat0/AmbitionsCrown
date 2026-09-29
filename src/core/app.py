import pygame

class App:
    def __init__(self):
        pygame.init()

        self.width = 1280
        self.height = 720

        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )

        pygame.display.set_caption("Ambitions Crown")

        self.clock = pygame.time.Clock()

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill((30, 30, 35))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(60)