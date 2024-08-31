import pygame as pg
import sys

class new_game:
    def __init__(self, s, b, tf, f):
        #starting variables
        self.screen = s
        self.background = b
        self.clock = pg.time.Clock()
        self.farm_name = ''
        self.font = f

        #Restarting the screen
        self.background.fill((248, 243, 241))
        text = tf.render("What is your digimon farm name?", True, (10,10,10))
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
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    if self.input_button.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False

                if event.type == pg.KEYDOWN and active:
                    
                    if event.key == pg.K_RETURN:
                        print(self.farm_name)
                        active = False

                    elif event.key == pg.K_BACKSPACE:
                        self.farm_name = self.farm_name[:-1]

                    else: 
                        self.farm_name += event.unicode

                        

            self.clock.tick(60)

            #rendering the screen
            text = self.font.render(self.farm_name, True, (10,10,10))
            self.background.blit(text, (self.input_button.x+5, self.input_button.y+5))
            self.screen.blit(self.background, (0,0))
            pg.display.flip()
        
