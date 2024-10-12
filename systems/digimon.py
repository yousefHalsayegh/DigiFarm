import pygame as pg
import random 
from sprite_sheet import SpriteSheet
import json

class Digimon:
    def __init__(self, data):

        self.name = data["Name"]
        self.type = data["Type"]
        self.attribute = data["Attribute"]
        self.level = data["Level"]
        self.speed = 10
        self.sprite_sheet = SpriteSheet("../Assests/digimons/"+self.level+"/"+self.name+".png")
        self.sprites = self.sprite_sheet.sprites()
        self.hit = pg.Rect(100,100,random.randint(16, 900),random.randint(16, 750))
        self.frame = 0
        self.target = pg.Rect(10,10,20,20)
        self.exp = 0
        self.next_level = 5
    
    def update(self, s, b):
        if self.reached():
            self.new_target()
            self.exp += 1
            print(self.exp)
            return
         
        if self.exp >= self.next_level:
           self.digivolve()
           self.exp = 0
           
        self.move(s,b)


    def move(self,s,b):
        x = 0 
        y = 0
        s.blit(b, self.hit)
        pg.draw.rect(s, (10,10,10), self.target)
        if self.target[0] > self.hit.left:
            x = 1 * self.speed 
        else: 
            x = -1 * self.speed 

        if self.target[1] > self.hit.top:
            y = 1 * self.speed 
        else: 
            y = -1 * self.speed 
        

        if self.hit.left + x <= 0 or self.hit.left + x + 16 >= 1000 : 
            x *= -1
        if self.hit.top + y <= 0 or self.hit.top + y + 16 >= 800:
            y *= -1
        self.frame  = 0 if self.frame == 1 else 1
        self.hit = self.hit.move(x,y)
        s.blit(self.sprites[self.frame], self.hit)

    def reached(self):
        return self.hit.colliderect(self.target)
    
    def new_target(self):
        self.target.left = random.randint(16, 950)
        self.target.top = random.randint(16, 750)

    def digivolve(self):
         with open('../Systems/tree.json', 'r') as file:
                tree = json.load(file)
                digi = tree[self.name][0]
                self.name = digi["Name"]
                self.attribute = digi["Attribute"]
                self.type = digi["Type"]
                self.level = digi["Level"]
                self.sprite_sheet = SpriteSheet("../Assests/digimons/"+self.level+"/"+self.name+".png")
                self.sprites = self.sprite_sheet.sprites()

    
        
        