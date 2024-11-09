from Systems.save_manager import SaveSystem 
from Systems.digimon import Digimon 


import pygame_gui as pg_gui
import pygame as pg
import sys

class Farm:
    def __init__(self,s, data):
        self.data = data
        self.screen = s

        self.save_manager = SaveSystem()

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        self.manager = pg_gui.UIManager((1000, 800), theme_path='assests/style/theme.json')

        self.clock = pg.time.Clock()
        
        self.digimons = []

        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):

        #Restarting the screen
        self.background.fill((248, 243, 241))
        self.screen.blit(self.background, (0,0))
        self.load()

    def run(self):
        while True:
            time_delta = self.clock.tick(6)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.manager.process_events(event)
            
        
            self.manager.update(time_delta)

            #rendering the screen
            
            self.manager.draw_ui(self.screen)
           
            for digimon in self.digimons:
             digimon.update(self.screen,self.background)
            
            
            pg.display.update()
            
    def load(self):
        for digimon in self.data["Digimon"]:
            digi = Digimon()
            digi.download(digimon)
            print(digi.upload())
            self.screen.blit(digi.sprites[0], digi.hit)
            self.digimons.append(digi)
            