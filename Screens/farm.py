#Other Modules
import pygame as pg
import sys
import pygame_gui as pg_gui

#Other Files
sys.path.insert(1, "../Systems")
from save_manager import SaveSystem 

class Farm:
    def __init__(self,s, data):
        self.data = data
        self.screen = s

        self.save_manager = SaveSystem(".mon", "save_data")

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        self.manager = pg_gui.UIManager((1000, 800), theme_path='../Assests/theme.json')

        self.clock = pg.time.Clock()
        
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        font = pg.font.Font(size=30)

        #Restarting the screen
        self.background.fill((248, 243, 241))

    def run(self):
        while True:
            time_delta = self.clock.tick(60)/1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.manager.process_events(event)
                
        
            self.manager.update(time_delta)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            pg.display.flip()
