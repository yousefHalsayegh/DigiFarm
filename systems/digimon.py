import pygame as pg
import random 
from sprite_sheet import SpriteSheet

class Digimon:
    def __init__(self, data):

        self.name = data["Name"]
        self.type = data["Type"]
        self.attribute = data["Attribute"]
        self.level = data["Level"]
        self.pos = (200,100)
        self.size = (10, 30)
        self.colour = (0,0,0)
        self.speed = 1
        self.sprite_sheet = SpriteSheet("../Assests/digimons/"+self.level+"/"+self.name+".png")
        self.sprites = self.sprite_sheet.sprites()
        
    
    
    def move(self, s, c):
        pass
        