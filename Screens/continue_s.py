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
        
        self.retun_button = pg_gui.elements.UIButton(pg.Rect(10, 10, 50, 40), text='Back', manager=self.manager)
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        self.background.fill((248, 243, 241))

        files = self.save_manager.files()
        self.container = pg_gui.elements.UIScrollingContainer(pg.Rect(self.background.get_width()/2-500,100,950,700), manager=self.manager, allow_scroll_x=False, object_id="container")
        
        for i in range(len(files)):
            pg_gui.elements.UITextBox(f'file name: {files[i]}', pg.Rect(20, (10+ (i * 60)), 800, 50),manager=self.manager,container=self.container).disable()
            pg_gui.elements.UIButton(pg.Rect(-100, (10+ (i * 60)), 50, 50), text='Start', manager=self.manager, object_id=f'start_{files[i][:-5]}',container=self.container, anchors={'right': 'right','top': 'top'})
            pg_gui.elements.UIButton(pg.Rect(-50, (10+ (i * 60)), 50, 50), text='Delete', manager=self.manager, object_id=f'end_{files[i][:-5]}',container=self.container,  anchors={'right': 'right','top': 'top'})
        

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
                        self.container.kill()
                        self.save_manager.delete(f'{event.ui_object_id[14:]}.json')
                        self.ui_start()
                    if "start_" in event.ui_object_id:
                        Farm(self.screen, self.save_manager.load_data(f'{event.ui_object_id[16:]}.json'))

                self.manager.process_events(event)
                
        
            self.manager.update(time_delta)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            pg.display.flip()
