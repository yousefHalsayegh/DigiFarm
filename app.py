import pygame as pg


def main():
    #Getting the screen ready
    pg.init()
    screen = pg.display.set_mode((1000,800), pg.SCALED)
    pg.display.set_caption("Digifarm")
    
    #intilazing the background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((248, 243, 241))

    clock = pg.time.Clock()
    running = True

    #To check if the font module is added correctly then do the thing
    if pg.font:
        #font initalize
        title_font = pg.font.Font(None, 72)
        text_font = pg.font.Font(None, 64)

        #Main Title
        text = title_font.render("DigiFarm", True, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2, y= 200)
        background.blit(text, textpos)

        #Start button
        pg.draw.rect(background, (164,164,164), pg.Rect((background.get_width()/2 - 150),270,300,50))
        text = text_font.render("Start", True, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2, y= 275)
        background.blit(text, textpos)

        


    #The run
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    
    
        clock.tick(60)

        #rendering the screen
        screen.blit(background, (0,0))
        pg.display.flip()
    pg.quit()


if __name__ == '__main__' :
    main()