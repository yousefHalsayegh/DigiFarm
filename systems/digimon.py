import pygame as pg
import random 
class Digimon:
    def __init__(self, data):
        self.name = data["Name"]
        self.type = data["Type"]
        self.family = data["Family"]
        self.core = data["Core"]
        self.pos = (200,100)
        self.size = (10, 30)
        self.colour = (0,0,0)
        self.speed = 1
        self.sprite = None
        self.rect =  self.sprite.get_rect()
    
    
    def move(self, b):
        self.rect.left += random.randint(0,10) * self.speed * random.randint(-1,1) 
        self.rect.top += random.randint(0,10) * self.speed * random.randint(-1,1)
        
        