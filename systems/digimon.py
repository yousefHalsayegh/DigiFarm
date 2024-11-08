import pygame as pg
import random 
from Systems.sprite_sheet import SpriteSheet
import json

class Digimon:
    def __init__(self, data, feeding):

        self.name = data["Name"]
        self.field = data["Field"]
        self.attribute = data["Attribute"]
        self.level = data["Level"]
        self.speed = 0
        self.sprite_sheet = SpriteSheet("Assests/digimons/"+self.level+"/"+self.name+".png")
        self.sprites = self.sprite_sheet.sprites()
        self.hit = pg.Rect(random.randint(16, 900),random.randint(116, 750),16,16)
        self.frame = 0
        self.target = pg.Rect(random.randint(20, 900),random.randint(120, 750),20,20)
        self.feeding_time = 10
        self.exp = 0
        self.next_level = 10
        self.hunger = 0
        self.starving = False
        self.feeding_area = feeding
        self.f = pg.font.Font(size=15)
        
    
    def update(self, s, b):
        self.debugging(s)
        if self.level == "digitama":
            if self.exp >= self.next_level :
                s.blit(self.sprites[2], self.hit)
            else:
                self.exp +=1

        if self.hunger >= 100 and not self.starving:
            self.new_target(s,'h')
            self.starving = True
        elif self.hunger <= 0 and self.starving:
            self.starving = False
            self.hunger = 0
            self.target = pg.Rect(random.randint(20, 900),random.randint(120, 750),20,20)
        elif not self.starving:
            self.hunger += 1 

        if self.reached(): 
            if self.starving:
                if self.feeding_time < 0 :
                    self.feeding_time = 10
                    self.hunger -= 10
                    self.exp += 1
                    return
                else:
                    self.feeding_time -= 1
                    self.frame  = 1 if self.frame == 2 else 2
                    s.blit(self.sprites[self.frame], self.hit)
                    return
            else:
                self.new_target(s)


        if self.exp >= self.next_level:
           self.digivolve()
           self.exp = 0
        
        
        self.move(s,b)
        

        


    def move(self,s,b):
        x = 0 
        y = 0
        s.blit(b, self.hit)
        pg.draw.rect(s, (10,10,10), self.target)
        
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
        self.frame  = 0 if self.frame == 1 else 1
        self.hit = self.hit.move(x,y)
        if x < 0 :
            s.blit(self.sprites[self.frame], self.hit)
        else:
            s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
        

    def reached(self):
        return self.hit.colliderect(self.target)
    
    def new_target(self, s, flag='r'):
        if flag == 'h':
            self.target = self.feeding_area
        else:
            pg.draw.rect(s, (248, 243, 241), self.target)
            self.target.left = random.randint(16, 950)
            self.target.top = random.randint(16, 750)

    def digivolve(self):
         with open('Systems/tree.json', 'r') as file:
                tree = json.load(file)
                digi = tree[self.name][0]
                self.name = digi["Name"]
                self.attribute = digi["Attribute"]
                self.field = digi["Type"]
                self.level = digi["Level"]
                self.speed = digi["Speed"]
                self.sprite_sheet = SpriteSheet("Assests/digimons/"+self.level+"/"+self.name+".png")
                self.sprites = self.sprite_sheet.sprites()
                self.hunger = 0 
                self.starving = False
                
    def debugging(self, s):
        
        pg.draw.rect(s, (248, 243, 241), rect=pg.Rect(0,0, 250,90))
        text = self.f.render(f'The digimon is currently at ({self.hit.left}, {self.hit.top}, {self.hit.left+16}, {self.hit.top+16})'
                             , True, (10,10,10))
        textpos = text.get_rect(x=5, y= 10)
        s.blit(text, textpos)

        text = self.f.render(f'The target is currently at ({self.target.left}, {self.target.top}, {self.target.left+20}, {self.target.top+20})'
                             , True, (10,10,10))
        textpos = text.get_rect(x=5, y= 20)
        s.blit(text, textpos)

        text = self.f.render(f'The current exp is {self.exp}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 30)
        s.blit(text, textpos)

        text = self.f.render(f'The target exp is {self.next_level}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 40)
        s.blit(text, textpos)

        text = self.f.render(f'starving {self.starving}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 50)
        s.blit(text, textpos)

        text = self.f.render(f'The hunger bar {self.hunger}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 60)
        s.blit(text, textpos)

        text = self.f.render(f'Feeding timer {self.feeding_time}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 70)
        s.blit(text, textpos)

        text = self.f.render(f'Am I at the target? {self.reached()}', True, (10,10,10))
        textpos = text.get_rect(x=5, y= 80)
        s.blit(text, textpos)
            
            
            

    
        
        