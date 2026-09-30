from Systems.save_manager import SaveSystem
import pygame_gui as pg_gui
import pygame as pg
from Screens.farm import Farm
import sys
class Continue:
    
    def __init__(self, s):
        """
        A class used to create the screen which allows the players to continue
        # Paramters 
        **s** : _pg.dispaly_ \n
        the surface which everything is drawn in, so that we don't have to open a new window
        """
        #starting variables

        #to refernce the same window 
        self.screen = s
        #to manipulate the save files
        self.save_manager = SaveSystem()

        #create a bacground similar to the background in the first page
        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        
        #UI manager to allow us to create UI elements and manipulate them 
        self.manager = pg_gui.UIManager((1000, 800), theme_path='assests/style/theme.json')
        #used for the frame rates
        self.clock = pg.time.Clock()

        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        """
        This method just cleans up the screen from previous information, and draws the UI elemtents for the Continue page
        """
        #"flashes" the screen to clear everything
        self.background.fill((248, 243, 241))

        #A button to allow you to go back to the main page
        self.retun_button = pg_gui.elements.UIButton(pg.Rect(10, 10, 50, 40), text='Back', manager=self.manager)

        #brings all the files inside the save folder
        files = self.save_manager.files()

        #the container holds in all the different save UIs to allow you to scroll through them and makes it dynamic
        self.container = pg_gui.elements.UIScrollingContainer(pg.Rect(self.background.get_width()/2-500,100,950,700), manager=self.manager, allow_scroll_x=False, object_id="container")

        #A loop whcih goes through the different save files and create the UI element for each
        for i in range(len(files)):
            #The element which contains the file name 
            pg_gui.elements.UITextBox(f'file name: {files[i]}', pg.Rect(20, (10+ (i * 60)), 800, 50),manager=self.manager,container=self.container).disable()
            #A button to start the game using this data
            pg_gui.elements.UIButton(pg.Rect(-100, (10+ (i * 60)), 50, 50), text='Start', manager=self.manager, object_id=f'start_{files[i][:-5]}',container=self.container, anchors={'right': 'right','top': 'top'})
            #A button to delete the file
            pg_gui.elements.UIButton(pg.Rect(-50, (10+ (i * 60)), 50, 50), text='Delete', manager=self.manager, object_id=f'end_{files[i][:-5]}',container=self.container,  anchors={'right': 'right','top': 'top'})
        

    def run(self):
        """
        This method is used to run the game and keeps refreshing to read any new event
        """
        while True:
            #The refresh rate
            time_delta = self.clock.tick(60)/1000
            
            #keeps reading new events
            for event in pg.event.get():
                #if the X is pressed to quit the game
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                
                #On a new button press the corresponding event occurs
                if event.type == pg_gui.UI_BUTTON_PRESSED:
                    #since this class is called after the "start" class a simple return will bring us back to the main page 
                    if event.ui_element == self.retun_button: 
                        return
                    #"end_" containers are the ones which are createrd to delete the file
                    if "end_" in event.ui_object_id:
                        self.container.kill()
                        self.save_manager.delete(f'{event.ui_object_id[14:]}.json')
                        files = self.save_manager.files()
                        for i in range(len(files)):
                            #The element which contains the file name 
                            pg_gui.elements.UITextBox(f'file name: {files[i]}', pg.Rect(20, (10+ (i * 60)), 800, 50),manager=self.manager,container=self.container).disable()
                            #A button to start the game using this data
                            pg_gui.elements.UIButton(pg.Rect(-100, (10+ (i * 60)), 50, 50), text='Start', manager=self.manager, object_id=f'start_{files[i][:-5]}',container=self.container, anchors={'right': 'right','top': 'top'})
                            #A button to delete the file
                            pg_gui.elements.UIButton(pg.Rect(-50, (10+ (i * 60)), 50, 50), text='Delete', manager=self.manager, object_id=f'end_{files[i][:-5]}',container=self.container,  anchors={'right': 'right','top': 'top'})
                    #"start" containers are the ones which load the data and start the game
                    if "start_" in event.ui_object_id:
                        Farm(self.screen, self.save_manager.load_data(f'{event.ui_object_id[16:]}.json'))
                
                #process the events
                self.manager.process_events(event)
                
            #listen to the events
            self.manager.update(time_delta)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            pg.display.flip()
