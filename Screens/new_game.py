#Other Modules
import pygame as pg
import sys
import pygame_gui as pg_gui

#Same File
from farm import Farm

#Other Files
sys.path.insert(1, "../Systems")
from save_manager import SaveSystem 

class NewGame:
    def __init__(self, s):
        #starting variables
        self.screen = s

        self.save_manager = SaveSystem(".mon", "save_data")

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        self.manager = pg_gui.UIManager((1000, 800), theme_path='../Assests/style/theme.json')

        self.clock = pg.time.Clock()
        self.farm_name = ''
        self.farm_type = ''
        self.digimon = {}
        
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):
        font = pg.font.Font(size=30)

        #Restarting the screen
        self.background.fill((248, 243, 241))
        text = font.render("What is your digimon farm name?", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 200)
        self.background.blit(text, textpos)
        text = font.render("Choose a farm type", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 280)
        self.background.blit(text, textpos)
        text = font.render("Choose a digiegg type", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 360)
        self.background.blit(text, textpos)
        text = font.render("What would you call your digitama?", True, (10,10,10))
        textpos = text.get_rect(centerx=self.background.get_width()/2, y= 440)
        self.background.blit(text, textpos)
        
        self.retun_button = pg_gui.elements.UIButton(pg.Rect(10, 10, 50, 40), text='Back', manager=self.manager)
        self.farm_input = pg_gui.elements.UITextEntryLine(pg.Rect((self.background.get_width()/2 - 150), 220, 300, 50), manager=self.manager)
        self.starting_farm = pg_gui.elements.UIDropDownMenu(['Dragon', 'Beast', 'Bird'],'Dragon', pg.Rect((self.background.get_width()/2 - 150), 300, 300, 50),manager=self.manager)
        self.starting_egg = pg_gui.elements.UIDropDownMenu(['Virus', 'Vaccine', 'Data'],'Virus', pg.Rect((self.background.get_width()/2 - 150), 380, 300, 50),manager=self.manager)
        self.name_input = pg_gui.elements.UITextEntryLine(pg.Rect((self.background.get_width()/2 - 150), 460, 300, 50), manager=self.manager)
        self.start = pg_gui.elements.UIButton(pg.Rect((self.background.get_width()/2 - 150), 540, 300, 50), text='Start', manager=self.manager)



    def run(self):
        while True:
            time_delta = self.clock.tick(60)/1000

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if event.type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.farm_input:
                        self.farm_name = event.text
                    if event.ui_element == self.name_input:
                        self.digimon["Name"]= event.text

                if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == self.starting_farm:
                        self.farm_type = event.text
                    if event.ui_element == self.starting_egg:
                        self.digimon["Type"] = event.text

                if event.type == pg_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.retun_button: 
                        return
                    if event.ui_element == self.start: 
                        self.save_manager.save_data({"Name": self.farm_name, "Type": self.farm_type, "Digimon" : self.digimon}, self.farm_name)
                        Farm(self.screen, {"Name": self.farm_name, "Type": self.farm_type, "Digimon" : self.digimon})


                self.manager.process_events(event)
                
        
            self.manager.update(time_delta)

            #rendering the screen
            self.screen.blit(self.background, (0,0))
            self.manager.draw_ui(self.screen)

            pg.display.flip()
