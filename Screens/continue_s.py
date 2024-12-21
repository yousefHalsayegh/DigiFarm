from Systems.save_manager import SaveSystem
import pygame_gui as pg_gui
import pygame as pg
from Screens.farm import Farm
import sys
class Continue:
    
    def __init__(self, s):
        #starting variables
        self.screen = s

        self.save_manager = SaveSystem()

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        

        self.manager = pg_gui.UIManager((1000, 800), theme_path='assests/style/theme.json')

        self.clock = pg.time.Clock()
        self.farm_name = ''
        
        
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        font = pg.font.Font(size=30)
        self.background.fill((248, 243, 241))

        files = self.save_manager.files()
        self.retun_button = pg_gui.elements.UIButton(pg.Rect(10, 10, 50, 40), text='Back', manager=self.manager)
        
        for i in range(len(files)):

            
            pg_gui.elements.UIButton(pg.Rect((self.background.get_width()/2 + 300), (200+ (i * 60)), 50, 50), text='Start', manager=self.manager, object_id=f'start_{files[i][:-5]}')
            pg_gui.elements.UIButton(pg.Rect((self.background.get_width()/2 + 350), (200+ (i * 60)), 50, 50), text='Delete', manager=self.manager, object_id=f'end_{files[i][:-5]}')
            pg.draw.rect(self.background, (200, 200, 200), pg.Rect((self.background.get_width()/2 - 400), (200+ (i * 60)), 800, 50))
            text = font.render(f'file name: {files[i]}', True, (10,10,10))
            textpos = text.get_rect(x=self.background.get_width()/2 - 400, y= (210 + (i * 60)))
            self.background.blit(text, textpos)

        

    def run(self):

        while True:
            time_delta = self.clock.tick(60)/1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
    
                if event.type == pg_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.retun_button: 
                        return
                    if "end_" in event.ui_object_id:
                        self.save_manager.delete(f'{event.ui_object_id[4:]}.json')
                        self.ui_start()
                    if "start_" in event.ui_object_id:
                        Farm(self.screen, self.save_manager.load_data(f'{event.ui_object_id[6:]}.json'))

                self.manager.process_events(event)
                
        
            self.manager.update(time_delta)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            pg.display.flip()
