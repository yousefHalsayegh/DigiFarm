from Systems.save_manager import SaveSystem 
from Systems.digimon import Digimon 
from Systems.digest import Digest

import pygame_gui as pg_gui
import pygame as pg
import sys
import json
import random
import numpy as np

class Farm:
    
    def __init__(self,s, data):
        """
        A class used to create the screen that contain the actual farm
        # Paramters 
        **s** : _pg.dispaly_ \n
        the surface which everything is drawn in, so that we don't have to open a new window \n
        **data** : _Dict_ \n
        Contain the information of the digimons in the farm 
        """
        #These are the fields used to breed new digimon
        self.fields = ['Dragon\'s Roar', 'Nightmare Soldiers']
        self.att = ['Virus']
        
        #contain the information fo each digimon
        self.data = data
        
        #the surface we draw on
        self.screen = s

        #The name of the Farm
        self.name = data["Name"]

        #The different hitboxes in the farm
        self.hitboxes = []

        #Used to save the game
        self.save_manager = SaveSystem()

        #To draw a background
        self.background = pg.Surface(s.get_size())
        self.background = self.background.convert()
        self.bg = pg.image.load('assests/background/back.png').convert()
        
        #To manage the UI elemetns
        self.manager = pg_gui.UIManager((1000, 800), theme_path='assests/style/theme.json')

        #For the refresh rate
        self.clock = pg.time.Clock()
       
        #The list of digimons in the farm
        self.digimons = []

        #A trigger to allow me debug the game
        self.debug = False

        #The amount of food in the farm
        self.food = data['Food']
        
        #Used to process the text given
        self.digest = Digest()
        
        #level editing
        self.edit = False

        #clean up the screen and add the inital UI 
        self.ui_start()
        
        #the map
        self.map = data['Map']
        self.breeding_area = self.map_edit(1)
        self.feeding_area = self.map_edit(3)
        self.moving_area = self.map_edit(0)
        self.not_allowed_area = self.map_edit(2)
        #getting into it
        try:
            self.run()
        except Exception as x:
            print("An error occured", x)
            self.save()


    def ui_start(self):
        """
        This method just cleans up the screen from previous information, and draws the UI elemtents for the Farm page
        """

        #Restarting the screen
        self.background.fill((248, 243, 241))
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.bg, (0,0))

        #This is a contianer used to allow the player to interact with the farm, mimicking a CMD and hiding it behind a button
        self.cmd = pg_gui.elements.UIScrollingContainer(pg. Rect(0,0, 1000, 800), manager=self.manager)
        self.cmd_text = pg_gui.elements.UITextBox("write 'help' in case you want to know all the comands", pg.Rect(10,10, 950, 740), manager=self.manager, container=self.cmd)
        self.input = pg_gui.elements.UITextEntryLine(pg.Rect(10,750,950,30), manager=self.manager, container=self.cmd)
        self.cmd.hide()
        #render all the present digimon
        self.load()


    def run(self):
        """
        The code which runs for the screen to function
        """
        held = -1
        while True:
            time_delta = self.clock.tick(6)

            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    self.save()
                    pg.quit()
                    sys.exit()
                
             

                if event.type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.input:
                        self.cmd_command(event.text)  
                        self.input.clear()
                        self.input.rebuild()
                if event.type ==  pg.KEYDOWN:
                    if event.key == pg.K_BACKQUOTE:
                        self.debug = not self.debug
                        if self.cmd.visible:
                            self.cmd.hide()
                            self.background.fill((248, 243, 241))
                            self.screen.blit(self.background, (0,0))
                            self.screen.blit(self.bg, (0,0))
                            self.input.focus()
                            self.cmd_text.set_text("")
                        else:
                            self.cmd.show()
                    if self.edit:
                        if event.key == pg.K_1:
                           self.edit_type = 'yes'
                        elif event.key == pg.K_2:
                            self.edit_type = 'no'
                        elif event.key == pg.K_3:
                           self.edit_type = 'food'
                if event.type == pg.MOUSEBUTTONDOWN and self.edit:
                    held = event.button
                elif event.type == pg.MOUSEBUTTONUP and self.edit:
                    held = -1
                if held != -1:
                    pos_x, pos_y = pg.mouse.get_pos()[0]//16,  pg.mouse.get_pos()[1]//16
                    color = (150,150,150)
                    if self.edit_type == "yes":
                        if held == 1:
                            self.map[pos_x][pos_y] = 1
                            color = (4, 40, 184)
                        elif held == 3:
                            self.map[pos_x][pos_y] = 0
                            color = (150,150,150)
                    elif self.edit_type == "no":
                        if held == 1:
                            self.map[pos_x][pos_y] = 2
                            color = (184, 4, 73)
                        elif held == 3:
                            self.map[pos_x][pos_y] = 0
                            color = (150,150,150)
                    elif self.edit_type == "food":
                        if held == 1:
                            self.map[pos_x][pos_y] = 3
                            color = (5, 161, 109)
                        elif held == 3:
                            self.map[pos_x][pos_y] = 0
                            color = (150,150,150)
                    
                    pg.draw.rect(self.screen,color, ((16*pos_x),(16*pos_y),16,16),1)
                

                self.manager.process_events(event)

                       
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            #rendering the screen
            if self.debug:
                pg.display.update()
                continue
            
            if self.edit:
                pg.display.update()
                continue
            
            dead = []
            self.screen.blit(self.bg, (0,0))
            for i in range(len(self.digimons)):
                n = self.digimons[i].update(self.screen,self.background, self.food, self.hitboxes)    
                if n is not None:
                    if n > 0 :
                        if self.digimons[n].dead(self.digimons[i].attack, self.screen, self.background):
                            dead.append(n)
                    elif self.food and (n == -1 or self.food[0][0] < 0) :
                        if self.food[0][0] < 0 :
                            self.food.pop()
                        else:
                            self.food[0][0] -= 1
                self.hitboxes[i] = self.digimons[i].hit

            for i in dead:
                self.digimons.pop(i)
                self.hitboxes.pop(i)
            
            pg.display.update()
            
    def load(self):
        self.digimons = []
        self.hitboxes = []
        for digimon in self.data["Digimon"]:
            digi = Digimon()
            digi.download(digimon)
            self.screen.blit(digi.sprites[0], digi.hit)
            self.digimons.append(digi)
            self.hitboxes.append(digi.hit)

    def save(self):
        digi = []
        for digimon in self.digimons:
            digi.append(digimon.upload())
        self.data["Digimon"] = digi
        self.data["Food"] = self.food 
        self.data["Map"] = self.map
        self.save_manager.save_data(self.data, self.name)

    #TODO: see if there is a better way to do this
    def cmd_command (self, text):
        t = text.split(" ")
        text = " ".join(t[1:])
        command = t[0].lower()
        if command == "help":
           self.cmd_text.set_text(self.cmd_text.html_text + 
                                """
help; showcase all the avaliable commands
feed; gives the ability to add to the data pile
list; gives a list of all the avaliable digimons
breed; this will allow to hatch a new egg using the data you have
data; showcase how much data you have
show; show the data of a specific digimon using the index of the digimon
kill; this kills a specific digimon using the index of the digimon
save; saves the current instance
edit; allows you to edit the level structure
exit; close the game""")  
        elif command == "save":
            self.save()
            self.cmd_text.set_text(self.cmd_text.html_text + "\nthe game has been saved ")
            self.load()
        elif command == "feed":
            food = self.digest.prepare(text)
            self.cmd_text.set_text(self.cmd_text.html_text + "\nthe following data has been added to the farm: '"+ text +"' giving an extra " +  str(food[0]) + " bytes of data")
            self.food.append(food)
        elif command == "list":
            self.cmd_text.set_text(self.cmd_text.html_text + "\ndigimon list:\n")
            for i in range(len(self.digimons)):
                self.cmd_text.set_text(self.cmd_text.html_text + str(i+1) +"."+self.digimons[i].name + "\n")
        elif command == 'data':
            self.cmd_text.set_text(self.cmd_text.html_text + "\nthe current amount of data we have is: " + str(self.food))
        elif command == "show":
             self.cmd_text.set_text(self.cmd_text.html_text + "\n" + self.digimons[int(t[1])-1].debugging())
        elif command == "kill":
            self.cmd_text.set_text(self.cmd_text.html_text + "\ngoodbye " + self.digimons[int(t[1])-1].name)
            self.digimons.pop(int(t[1])-1)
            self.hitboxes.pop(int(t[1])-1)
        elif command == "breed":
            if self.food:
                name = ""
                f = random.choice(self.fields)
                att = self.food[0][1]
                with open('Systems/starting_eggs.json', 'r') as file:
                    eggs = json.load(file)
                    name = eggs[f][att][0]
                new_digi = Digimon(name, f, att)
                new_digi.fast_download()
                new_digi.exp = self.food[0][0]
                self.digimons.append(new_digi)
                self.hitboxes.append(new_digi.hit)
                self.food.pop()
                self.cmd_text.set_text(self.cmd_text.html_text + f'\nthe following digimon has been added to the farm: {new_digi.name}')
            else:
                self.cmd_text.set_text(self.cmd_text.html_text + "\nnot enough data")
        elif command == "edit":
            if self.edit:
                self.edit = False
                self.ui_start()
                self.breeding_area = self.map_edit(1)
                self.feeding_area = self.map_edit(3)
                self.moving_area = self.map_edit(0)
                self.not_allowed_area = self.map_edit(2)
            else:
                self.edit = True
                self.cmd.hide()
                self.background.fill((248, 243, 241))
                self.screen.blit(self.background, (0,0))
                self.screen.blit(self.bg, (0,0))
                self.input.focus()
                self.cmd_text.set_text("")
                self.banner = pg_gui.elements.UILabel(pg.Rect((self.background.get_width()/2 - 150), -10, 300, 50), "EDITING MODE", self.manager)
                self.lower = pg_gui.elements.UILabel(pg.Rect((self.background.get_width()/2 - 200), -20, 450, 100), "1 for walkable tiles, 2 for unwalkable tiles, 3 for the food source", self.manager)
                self.edit_type = 'yes'
                for i in range(len(self.map)):
                    for j in range(len(self.map[0])):
                        color = (255,255,255)
                        if self.map[i][j] == 0:
                            color = (150, 150, 150)
                        elif self.map[i][j] == 1:
                            color = (4, 40, 184)
                        elif self.map[i][j] == 2:
                            color = (184, 4, 73)
                        elif self.map[i][j] == 3:
                            color = (5, 161, 109)
                        pg.draw.rect(self.screen,color, ((16*i),(16*j),16,16),1)
        elif command == "exit":
            self.save()
            pg.quit()
            sys.exit()
        else:
            self.cmd_text.set_text(self.cmd_text.html_text + "\n"+ command +" is not a known command has been added, please try again")



    def map_edit(self, n):
        find = []
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == n:
                    find.append((i,j))
        return find