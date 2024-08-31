import pygame as pg
import sys
import pygame_gui as pg_gui

class new_game:
    def __init__(self, s, tf, f):
        #starting variables
        self.screen = s

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        self.manager = pg_gui.UIManager((1000, 800), theme_path='theme.json')

        self.clock = pg.time.Clock()
        self.farm_name = ''
        self.font = f

        #Restarting the screen
        self.background.fill((248, 243, 241))
        text = tf.render("What is your digimon farm name?", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 200)
        self.background.blit(text, textpos)
        
        self.input_field = pg_gui.elements.UITextEntryLine(pg.Rect((self.background.get_width()/2 - 150), 270, 300, 50), manager=self.manager)
        #getting into it
        self.run()

    def run(self):
        active = False
        while True:
            time_delta = self.clock.tick(60)/1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                    self.farm_name = event.text
                    print(self.farm_name)

                self.manager.process_events(event)
                
        
            self.manager.update(time_delta)
            self.clock.tick(60)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.background)

            pg.display.flip()
