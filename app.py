import pygame as pg



pg.init()

screen = pg.display.set_mode((1000,800))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
   
   
    clock.tick(60)

pg.quit()