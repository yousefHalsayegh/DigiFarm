import pygame as pg
import random 
from Systems.sprite_sheet import SpriteSheet
import json

class Digimon:
    def __init__(self, name = "Guil_Digitama", field = "", attribute = "", level = "digitama"):

        self.name = name
        self.field = field
        self.attribute = attribute 
        self.level = level
        self.speed = 0
        self.sprites = None
        self.frame = 0
        self.feeding_time = 10
        self.exp = 0
        self.next_level = 10
        self.hunger = 100
        self.state = "Walking"
        self.feeding_area = (500, 400, 100, 100)
        self.hit = (random.randint(16, 900),random.randint(116, 750),16,16)
        self.target = (random.randint(20, 900),random.randint(120, 750),20,20)
        self.energy = 100
        self.facing = 1
        self.debug = False
        self.counter = 0 
        
    

    
    def update(self, s, b):
        if self.debug:
            self.debugging(s)
        

        #egg state
        if self.level == "digitama":
            if self.exp >= self.next_level :
                s.blit(self.sprites[2], self.hit)
            else:
                self.exp +=1

        #behaviour
        if self.state == "Sleepy":
            if self.energy > 100: 
                self.state = "Walking"
                return
            else:
                self.energy += 1
                self.frame  = 4 if self.frame == 5 else 5
                if self.facing < 0:
                    s.blit(self.sprites[self.frame], self.hit)
                else: 
                    s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
                return
            
        elif self.state == "Starving":
            if self.hunger > 100:
                self.state = "Walking"
                self.target = pg.Rect(random.randint(20, 900),random.randint(120, 750),20,20)
                self.speed *= 2
            elif self.reached():
                if self.feeding_time < 0 :
                    self.feeding_time = 10
                    self.hunger += 10
                    self.exp += 1
                    return
                else:
                    self.feeding_time -= 1
                    self.frame  = 2 if self.frame == 3 else 3
                    if self.facing < 0 :
                        s.blit(self.sprites[self.frame], self.hit)
                    else :
                        s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
                    return
            else:
                self.move(s,b)
        elif self.state == "Idle":
            if self.counter > 0 :
                self.frame  = 7 if self.frame == 3 else 3
                if self.facing < 0 :
                    s.blit(self.sprites[self.frame], self.hit)
                else :
                    s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
                self.counter -= 3
            else:
                self.state = "Walking"

        elif self.state == "Walking":       
            if self.energy < 0 :
                self.state = "Sleepy"
                return
            elif self.hunger < 0:
                self.new_target(s,'h')
                self.state = "Starving"
                self.speed /= 2
            elif self.reached():
                self.new_target(s)
            elif self.counter >= 10:
                self.state = "Idle"

            self.energy -= 1
            self.hunger -= 1
            self.counter += 1
            self.move(s,b)


        #digivolve
        if self.exp >= self.next_level:
           self.digivolve()
           
        

    def move(self,s,b):
        x = 0 
        y = 0
        s.blit(b, self.hit)
        
        if self.target.left > self.hit.left and self.target.right > self.hit.right:
            x = 1 * self.speed 
        elif self.target.left < self.hit.left and self.target.right < self.hit.right: 
            x = -1 * self.speed 

        if self.target.top > self.hit.top and self.target.bottom > self.hit.bottom:
            y = 1 * self.speed 
        elif self.target.top < self.hit.top and self.target.bottom < self.hit.bottom: 
            y = -1 * self.speed 
        

        if self.hit.left + x <= 0 or self.hit.left + x + 16 >= 1000 : 
            x *= -1
        if self.hit.top + y <= 0 or self.hit.top + y + 16 >= 800:
            y *= -1
        if self.state == "Starving":
            self.frame  = 9 if self.frame == 10 else 10
        else:
            self.frame  = 0 if self.frame == 1 else 1
        self.hit = self.hit.move(x,y)
        if x < 0 :
            s.blit(self.sprites[self.frame], self.hit)
            self.facing = -1
        else:
            s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
            self.facing = 1
        

    def reached(self):
        return self.hit.colliderect(self.target)
    
    def new_target(self, s, flag='r'):
        if flag == 'h':
            self.target = self.feeding_area
        else:
            pg.draw.rect(s, (248, 243, 241), self.target)
            self.target.left = self.hit.left + random.randint(-50, 50)
            self.target.top = self.hit.top + random.randint(-50, 50)

    def digivolve(self):
         with open('Systems/tree.json', 'r') as file:
                tree = json.load(file)
                digi = tree[self.name][0]
                self.name = digi["Name"]
                self.attribute = digi["Attribute"]
                self.field = digi["Type"]
                self.level = digi["Level"]
                self.speed = digi["Speed"]
                self.render()
                self.hunger = 100
                self.energy = 100
                self.state = "Walking"
                self.exp = 0
                self.next_level = 1000


    def upload(self):
        self.sprites = None
        print(type(self.hit))
        if type(self.hit) is not tuple:
            self.feeding_area = (500, 400, 100, 100)
            self.hit = (self.hit.left, self.hit.top, 16, 16) 
            self.target = (self.target.left, self.target.top, 20, 20) 
        return self.__dict__
    
    def download(self, data):
        for key in data :
            setattr(self, key, data[key])

        self.target = pg.Rect(self.target)
        self.feeding_area = pg.Rect(self.feeding_area)
        self.hit = pg.Rect(self.hit)
        self.render()
        


    def render(self):
        self.sprites = SpriteSheet("Assests/digimons/"+self.level+"/"+self.name+".png").sprites()

    

    def debugging(self, s):
        f = pg.font.Font(size=15)
        
        pg.draw.rect(s, (248, 243, 241), rect=pg.Rect(0,0, 250,100))
        text = f.render(f'The digimon is currently at ({self.hit.left}, {self.hit.top}, {self.hit.left+16}, {self.hit.top+16})'
                             , True, (10,10,10))
        textpos = text.get_rect(x=5, y= 10)
        s.blit(text, textpos)

        text = f.render(f'The target is currently at ({self.target.left}, {self.target.top}, {self.target.left+20}, {self.target.top+20})'
                             , True, (10,10,10))
        textpos = text.get_rect(x=5, y= 20)
        s.blit(text, textpos)

        text = f.render(f'The current exp is {self.exp}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 30)
        s.blit(text, textpos)

        text = f.render(f'The target exp is {self.next_level}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 40)
        s.blit(text, textpos)

        text = f.render(f'starving {self.state}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 50)
        s.blit(text, textpos)

        text = f.render(f'The hunger bar {self.hunger}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 60)
        s.blit(text, textpos)

        text = f.render(f'Feeding timer {self.feeding_time}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 70)
        s.blit(text, textpos)

        text = f.render(f'My energy is at? {self.energy}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 80)
        s.blit(text, textpos)

        text = f.render(f'Am I at the target? {self.reached()}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 90)
        s.blit(text, textpos)

        
            
            
            

    
        
        