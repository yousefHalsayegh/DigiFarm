#Other Modules
import pygame as pg
import sys
sys.path.insert(0,"..\\systems")

import pygame_gui as pg_gui
import json
from Screens.farm import Farm
from Systems.save_manager import SaveSystem 
from Systems.digimon import Digimon

class NewGame:

    def __init__(self, s):
        """
        A class used to create the screen which allows the players to start a new game
        # Paramters 
        **s** : _pg.dispaly_ \n
        the surface which everything is drawn in, so that we don't have to open a new window
        """
        #starting variables
        #The surface stuff is built on
        self.screen = s
        #From the `save_manager.py` class which allow us to save the game
        self.save_manager = SaveSystem()

        #"clean up" the screen to start on a blank screen
        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        #The UI manager which allow us control the UI elements
        self.manager = pg_gui.UIManager((1000, 800), theme_path='assests/style/theme.json')

        #Clock used for the rate
        self.clock = pg.time.Clock()

        #Initial farm information 
        self.farm_name = ''
        self.eggs = ''
        self.fields = []
        self.att = []
        self.eggs_start()
        
        #clean up the screen and add the inital UI 
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        """
        This method just cleans up the screen from previous information, and draws the UI elemtents for the New Game page
        """
         
        #The font which is used in the text
        font = pg.font.Font(size=30)

        #Restarting the screen
        self.background.fill((248, 243, 241))

        #The inital input for the farm

        # this is for the text labels
        text = font.render("What is your digimon farm name?", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 200)
        self.background.blit(text, textpos)
        text = font.render("Choose a Digimon field", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 280)
        self.background.blit(text, textpos)
        text = font.render("Choose a Digimon atrribute", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 360)
        self.background.blit(text, textpos)
        
        #This is for the buttons and drop down for the farm
        self.retun_button = pg_gui.elements.UIButton(pg.Rect(10, 10, 50, 40), text='Back', manager=self.manager)
        self.farm_input = pg_gui.elements.UITextEntryLine(pg.Rect((self.background.get_width()/2 - 150), 220, 300, 50), manager=self.manager)
        self.starting_field = pg_gui.elements.UIDropDownMenu(
            self.fields
            ,self.fields[0], pg.Rect((self.background.get_width()/2 - 150), 300, 300, 50),manager=self.manager)
        self.starting_attribute = pg_gui.elements.UIDropDownMenu(
            self.att,
            self.att[0], pg.Rect((self.background.get_width()/2 - 150), 380, 300, 50),manager=self.manager)
        self.start = pg_gui.elements.UIButton(pg.Rect((self.background.get_width()/2 - 150), 540, 300, 50), text='Start', manager=self.manager)

        

    def run(self):
        """
        The code which runs for the screen to function
        """

        #Here since the digimon class needs to have something for us to save, this is basically the defualt info 
        digimon = Digimon(field="Dragon\'s Roar", attribute="Virus", level="digitama")
        while True:
            #The refresh rate
            time_delta = self.clock.tick(60)/1000

            for event in pg.event.get():
                #in case the X is pressed to close the game
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                        
                #Used to pick the attribute and field of the digimon
                if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.starting_attribute:
                        digimon.attribute = event.text
                    if event.ui_element == self.starting_field:
                        digimon.field = event.text
                        self.att = list(self.eggs[event.text].keys())
                        self.starting_attribute.options_list = self.att
                        self.starting_attribute.kill()
                        self.starting_attribute = pg_gui.elements.UIDropDownMenu(
                            self.att,
                            self.att[0], pg.Rect((self.background.get_width()/2 - 150), 380, 300, 50),manager=self.manager)
                        
                if event.type == pg_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.retun_button: 
                        return
                    if event.ui_element == self.start: 
                        if self.farm_input.get_text() == "":
                            #TODO add a error message better
                            self.farm_name == "na"
                        else:
                            self.farm_name = self.farm_input.get_text()
                        #takes a random egg from eggs present in the eggs json
                        #TODO: make the picking random on the egg 
                        digimon.name = self.eggs[digimon.field][digimon.attribute][0]

                        #do the initial save and start the game
                        self.save_manager.save_data({"Name" : self.farm_name, "Digimon" : [digimon.upload()]}, self.farm_name)
                        Farm(self.screen, {"Name" : self.farm_name,"Digimon" : [digimon.upload()], "Food" : [[0, 'Data']]})

                #process the events
                self.manager.process_events(event)
                
            #listen to the events
            self.manager.update(time_delta)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            pg.display.flip()


    def eggs_start(self):
        """
        This method reads from the `starting_eggs.json` to extract the possible eggs you can have as our first digimon
        """
        with open('Systems/starting_eggs.json', 'r') as file:
                self.eggs = json.load(file)
                self.fields = list(self.eggs.keys())
                self.att = list(self.eggs[self.fields[0]].keys())