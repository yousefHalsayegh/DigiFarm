import pygame as pg
import pygame_gui as pg_gui
from new_game import new_game as ng
import sys



def main():
    #Getting the screen read
    WIDTH = 1000
    HEIGHT = 800
    screen = pg.display.set_mode((WIDTH,HEIGHT), pg.SCALED)
    pg.display.set_caption("Digifarm")
    
    #intilazing the background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((248, 243, 241))

    #UI manager
    manager = pg_gui.UIManager((WIDTH, HEIGHT), theme_path='theme.json')
    clock = pg.time.Clock()


    #To check if the font module is added correctly then do the thing
    if pg.font:
        #font initalize
        title_font = pg.font.Font(None, 72)
        text_font = pg.font.Font(None, 64)

        #Main Title
        text = title_font.render("DigiFarm", True, (10,10,10))
        textpos = text.get_rect(centerx=background.get_width()/2, y= 200)
        background.blit(text, textpos)

        #Buttons hitbox
        start_button = pg_gui.elements.UIButton(pg.Rect((background.get_width()/2 - 150), 270, 300, 50), text='New Game', manager=manager)
        load_button = pg_gui.elements.UIButton(pg.Rect((background.get_width()/2 - 150), 340, 300, 50), text='Continue', manager=manager)
        setting_button = pg_gui.elements.UIButton(pg.Rect((background.get_width()/2 - 150), 410, 300, 50), text='Settings', manager=manager)
        exit_button = pg_gui.elements.UIButton(pg.Rect((background.get_width()/2 - 150), 480, 300, 50), text='Exit', manager=manager)

    
        


    #The run
    while True:
        time_delta = clock.tick(60)/1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    ng(screen, title_font, text_font)
                    
                elif event.ui_element == load_button:
                    print("Load game")
                elif event.ui_element == setting_button:
                    print("Settings")
                elif event.ui_element == exit_button:
                    pg.quit()
                    sys.exit()


            manager.process_events(event)
            
    
        manager.update(time_delta)
        clock.tick(60)

        #rendering the screen
        screen.blit(background, (0,0))
        manager.draw_ui(background)

        pg.display.flip()
    


if __name__ == '__main__' :
    pg.init()
    main()