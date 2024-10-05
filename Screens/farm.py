#Other Modules
import pygame as pg
import sys
import pygame_gui as pg_gui

#Other Files
sys.path.insert(1, "../systems")
from save_manager import SaveSystem 
from digimon import Digimon

class Farm:
    def __init__(self,s, data):
        self.data = data
        self.screen = s

        self.save_manager = SaveSystem()

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        self.manager = pg_gui.UIManager((1000, 800), theme_path='../assests/style/theme.json')

        self.clock = pg.time.Clock()
        self.digimons = []
        
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        font = pg.font.Font(size=30)

        #Restarting the screen
        self.background.fill((248, 243, 241))
        self.screen.blit(self.background, (0,0))
        self.load()

    def run(self):
        last_update = pg.time.get_ticks()
        frame = 0
        while True:
            time_delta = self.clock.tick(60)/1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                self.manager.process_events(event)
            
        
            self.manager.update(time_delta)

            #rendering the screen
            
            self.manager.draw_ui(self.screen)

            current_time = pg.time.get_ticks()
            if current_time - last_update >= 600:
                frame += 1
                if frame >= len(self.digimons[0].sprites):
                    frame = 0
                last_update = current_time

            self.screen.blit(self.digimons[0].sprites[frame], (10,10))
            
            pg.display.flip()
            
    def load(self):
        for digi in self.data["Digimon"]:
            digimon = Digimon(digi)
            self.screen.blit(digimon.sprites[0], (10,10))
            self.digimons.append(digimon)