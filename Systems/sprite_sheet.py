import pygame as pg


class SpriteSheet:
    def __init__(self, filename):
        
        try:
            self.sheet = pg.image.load(filename).convert()

        except pg.error as e:
            print(f'Unable to find the following file {filename}')
            raise SystemError(e)

        
    def sprites(self):
        images = []
        for i in range(4):
            for j in range(3):
                #get the idle image
                image = pg.Surface((16,16)).convert()
                image.blit(self.sheet, (0,0), ((j * 16),(i * 16), 16, 16))

                #change the size
                image = pg.transform.scale(image, (48, 48))
                images.append(image)

        return images