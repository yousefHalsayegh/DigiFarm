import pygame as pg

class new_game:
    def __init__(self, s, b):
        self.screen = s
        self.background = b.fill((0,0,0))
        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.clock.tick(60)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            pg.display.flip()
        pg.quit()
