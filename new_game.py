import pygame as pg

class new_game:
    def __init__(self, s, b, f):
        #starting variables
        self.screen = s
        self.background = b
        self.clock = pg.time.Clock()

        #Restarting the screen
        self.background.fill((248, 243, 241))
        text = f.render("What is your digimon farm name?", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 200)
        self.background.blit(text, textpos)
        
        #getting into it
        self.run()

    def run(self):
        active = False
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.clock.tick(60)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            pg.display.flip()
        
