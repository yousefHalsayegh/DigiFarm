import pygame as pg
import random 
from sprite_sheet import SpriteSheet

class Digimon:
    def __init__(self, data):

        self.name = data["Name"]
        self.type = data["Type"]
        self.attribute = data["Attribute"]
        self.level = data["Level"]
        self.speed = 3
        self.sprite_sheet = SpriteSheet("../Assests/digimons/"+self.level+"/"+self.name+".png")
        self.sprites = self.sprite_sheet.sprites()
        self.hit = pg.Rect(100,100,16,16)
        self.frame = 0
        
    
    
    def move(self,s,b):
        s.blit(b, self.hit)
        x = random.randint(-1, 1) * self.speed 
        y = random.randint(-1,1)* self.speed 

        if self.hit.left + x <= 0 or self.hit.left + x + 16 >= 1000 : 
            x *= -1
        if self.hit.top + y <= 0 or self.hit.top + y + 16 >= 800:
            y *= -1
        self.frame  = 0 if self.frame == 1 else 1
        self.hit = self.hit.move(x,y)
        s.blit(self.sprites[self.frame], self.hit)
        
        