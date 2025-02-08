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
        self.hit = (random.randint(16, 900),random.randint(116, 600),16,16)
        self.target = (random.randint(20, 900),random.randint(120, 600),20,20)
        self.energy = 100
        self.facing = 1
        self.counter = 0 
        self.feeding_area =(500, 400, 100, 100)
        self.health = 3
        self.attack = 1
        self.coll = 0
        self.nature = {"Virus": 0, "Data":0, "Vaccine":0}

    
    def update(self, s, b, food, hits):
        nature = ""
        if food:   
            nature = food[0][1]
            food = food[0][0]
        else:
            food = -1
            

        #egg state
        if self.level == "digitama":
            if self.exp >= self.next_level :
                s.blit(self.sprites[2], self.hit)
            else:
                self.exp +=1
        #digivolve
        if self.exp >= self.next_level:
            self.digivolve()

        self.coll = self.hit.collidelist(hits)
        if self.coll >= 0 :
            if not(self.hit == hits[self.coll]):
                self.state = "Attack"
                return self.coll
        
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
            if food > 0 and not (self.target == self.feeding_area):
                self.new_target(s, 'h')
            if self.hunger > 100:
                self.state = "Walking"
                self.target = self.new_target(s)
                self.speed *= 2
            elif self.reached():
                if food < 0 :
                    self.new_target(s)
                elif self.feeding_time < 0 :
                    self.feeding_time = 10
                    self.hunger += 10
                    self.exp += 1
                    food -= 1
                    self.nature[nature] += 1
                    return -1
                else:
                    self.feeding_time -= 1
                    self.frame  = 2 if self.frame == 3 else 3
                    if self.facing < 0 :
                        s.blit(self.sprites[self.frame], self.hit)
                    else :
                        s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
                    return
            else:
                self.move(s,b, hits)
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
        elif self.state == "Attack":
            self.coll = self.hit.collidelist(hits)
            if self.coll >= 0 :
                if not(self.hit == hits[self.coll]):
                    self.frame  = 8 if self.frame == 11 else 11
                    if self.facing < 0 :
                        s.blit(self.sprites[self.frame], self.hit)
                    else :
                        s.blit(pg.transform.flip(self.sprites[self.frame], True, False), self.hit)
                    return self.coll
                else:
                    self.state = "Walking"
        elif self.state == "Walking":       
            if self.energy < 0 :
                self.state = "Sleepy"
                return
            elif self.hunger < 0:
                if food > 0 :
                    self.new_target(s,'h')
                else:
                    self.new_target(s)
                self.state = "Starving"
                self.speed /= 2
            elif self.reached():
                self.new_target(s)
            elif self.counter >= 10:
                self.state = "Idle"

            self.energy -= 1
            self.hunger -= 1
            self.counter += 1
            self.move(s,b, hits)


       
           
    def dead (self, a, s, b):

        self.health -= a 
        if self.health <= 0:
            s.blit(b,self.hit, area=self.hit)
            return True

    def move(self,s,b, hits):
        x = 0 
        y = 0
        s.blit(b,self.hit, area=self.hit)
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
        
        self.coll = self.hit.collidelist(hits)
        if self.coll >= 0 :
           if not(self.hit == hits[self.coll]):
              self.state = "Attack"
              return 
           

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
            self.target = pg.Rect(self.feeding_area)
        else:
            pg.draw.rect(s, (248, 243, 241), self.target)
            self.target.left = self.hit.left + random.randint(-20, 20)
            self.target.top = self.hit.top + random.randint(-20, 20)

    def digivolve(self):
         with open('Systems/tree.json', 'r') as file:
                tree = json.load(file)
                digi = tree[self.level][self.name][0]
                for key in digi :
                    setattr(self, key, digi[key])
                self.render()
                self.hunger = 100
                self.energy = 100
                self.state = "Walking"
                self.exp = 0


    def upload(self):
        self.sprites = None
        self.coll= 0
        if type(self.hit) is not tuple:
            self.hit = (self.hit.left, self.hit.top, 16, 16) 
            self.target = (self.target.left, self.target.top, 20, 20) 
            self.feeding_area = (500, 400, 100, 100)
        return self.__dict__
    
    def download(self, data):
        for key in data :
            setattr(self, key, data[key])
        self.fast_download()
        

    def fast_download(self):
        self.target = pg.Rect(self.target)
        self.hit = pg.Rect(self.hit)
        self.feeding_area = pg.Rect(self.feeding_area)
        self.render()
        
        


    def render(self):
        self.sprites = SpriteSheet("Assests/digimons/"+self.level+"/"+self.name+".png").sprites()

    

    def debugging(self):

        return f'{self.__dict__}'