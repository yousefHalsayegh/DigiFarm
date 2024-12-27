from Systems.save_manager import SaveSystem 
from Systems.digimon import Digimon 


import pygame_gui as pg_gui
import pygame as pg
import sys
import json
import random

class Farm:
    
  

    def __init__(self,s, data):

        self.fields = ['Dragon\'s Roar', 'Nightmare Soldiers']
        self.att = ['Virus']

        self.data = data
        self.screen = s
        self.name = data["Name"]
        self.hitboxes = []
        self.save_manager = SaveSystem()

        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.background.fill((248, 243, 241))

        self.manager = pg_gui.UIManager((1000, 800), theme_path='assests/style/theme.json')

        self.clock = pg.time.Clock()
        
        self.digimons = []
        self.debug = False
        self.food = data['Food']
        self.ui_start()
        #getting into it
        self.run()

    def ui_start(self):

        #Restarting the screen
        self.background.fill((248, 243, 241))
        self.screen.blit(self.background, (0,0))

        self.input = pg_gui.elements.UITextEntryLine(pg.Rect(10,750,900,30), manager=self.manager)

        self.update_food()

        self.load()


    def run(self):
        while True:
            time_delta = self.clock.tick(6)

            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    digi = []
                    for digimon in self.digimons:
                        digi.append(digimon.upload())
                    self.data["Digimon"] = digi
                    self.data["Food"] = self.food 
                    self.save_manager.save_data(self.data, self.name)
                    pg.quit()
                    sys.exit()
                    
                if event.type ==  pg.KEYDOWN:
                    if event.key == pg.K_F1:
                        self.debug = not self.debug
                    if event.key == pg.K_ESCAPE:
                        if self.input.visible:
                            self.input.hide()
                            pg.draw.rect(self.screen, (248, 243, 241), (10,750,900,30))
                        else:
                            self.input.show()
                    if event.key == pg.K_F2:
                        if self.food > 20:
                            name = ""
                            f = random.choice(self.fields)
                            att = random.choice(self.att)
                            with open('Systems/starting_eggs.json', 'r') as file:
                                eggs = json.load(file)
                                name = eggs[f][att][0]
                            new_digi = Digimon(name, f, att)
                            new_digi.fast_download()
                            self.digimons.append(new_digi)
                            self.hitboxes.append(new_digi.hit)
                            self.food -= 20
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.debug:  
                    for digimon in self.digimons:
                        if digimon.hit.collidepoint(pg.mouse.get_pos()):
                            digimon.debug = not digimon.debug
                            if not digimon.debug:
                                pg.draw.rect(self.screen, (248, 243, 241), rect=pg.Rect(0,0, 250,100)) 
                if event.type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.input:
                        self.food += len(event.text)  
                        self.input.clear()
                        self.input.rebuild()

                        
                if not self.debug:
                    for digimon in self.digimons:
                        digimon.debug = False
                    pg.draw.rect(self.screen, (248, 243, 241), rect=pg.Rect(0,0, 250,100)) 

                self.manager.process_events(event)
            
            self.update_food()
                       
            self.manager.update(time_delta)

            #rendering the screen
            
            self.manager.draw_ui(self.screen)
           
            for i in range(len(self.digimons)):
               
                if self.digimons[i].update(self.screen,self.background, self.food, self.hitboxes) is not None:
                    self.food -= 1
                self.hitboxes[i] = self.digimons[i].hit
            
            
            pg.display.update()
            
    def load(self):
        for digimon in self.data["Digimon"]:
            digi = Digimon()
            digi.download(digimon)
            self.screen.blit(digi.sprites[0], digi.hit)
            self.digimons.append(digi)
            self.hitboxes.append(digi.hit)
    def update_food(self):
        pg.draw.rect(self.screen, (248, 243, 241), rect=pg.Rect(870,10, 150,10))
        text = pg.font.Font(size=15).render(f'food current is at:  {self.food}'
                            , True, (10,10,10))
        textpos = text.get_rect(x=870, y= 10)
        self.screen.blit(text, textpos)