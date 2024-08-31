import pygame as pg
from new_game import new_game as ng

def check_hitbox(pos, hitbox):
    return pos[0] < hitbox[0] and pos[0] > hitbox[2] and  pos[1] < hitbox[1] and  pos[1] > hitbox[3]

def create_button(background, text_font, label, x, y, w=300, h=50):

    #button rectangle "skeleton"
    button = pg.Rect(x,y,w,h)

    #(x1, y1, x2, y2) to track the hitbox 
    hitbox = button.bottomright + button.topleft

    #button UI
    pg.draw.rect(background, (164,164,164),button )
    text = text_font.render(label, True, (10,10,10))
    textpos = text.get_rect(centerx=background.get_width()/2, y= y+5)

    background.blit(text, textpos)

    return hitbox

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

        #Buttons hitbox
        start_button_hitbox = create_button(background, text_font, "New Game", (background.get_width()/2 - 150), 270)
        load_button_hitbox = create_button(background, text_font, "Continue", (background.get_width()/2 - 150), 340)
        setting_button_hitbox = create_button(background, text_font, "Settings", (background.get_width()/2 - 150), 410)
        exit_button_hitbox = create_button(background, text_font, "Exit", (background.get_width()/2 - 150), 480)
        
    
        


    #The run
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if check_hitbox(pos, start_button_hitbox):
                    ng(screen, background)
                    
                elif check_hitbox(pos, load_button_hitbox):
                    print("Load game")
                elif check_hitbox(pos, setting_button_hitbox):
                    print("Settings")
                elif check_hitbox(pos, exit_button_hitbox):
                    running = False
    
    
        clock.tick(60)

        #rendering the screen
        screen.blit(background, (0,0))
        pg.display.flip()
    pg.quit()


if __name__ == '__main__' :
    main()