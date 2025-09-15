import pygame as pg


class SpriteSheet:
    def __init__(self, filename):
        """
        This class is used to read the different sprite sheets in the digi folder which allows to render their animations 
        # Parameter:
        **filename** : _str_ \n
        The digimon file name which contains the spirtie sheet
        """
        try:
            #this loads the full sprite sheet
            self.sheet = pg.image.load(filename).convert()

        except pg.error as e:
            print(f'Unable to find the following file {filename}')
            raise SystemError(e)

        
    def sprites(self):
        """
        This method breaks down the spirite sheet into "slides" which makes it easier to render

        # Return
        **images** : _list_
        This contain the different sprities that has been extracted from the spritie sheet
        """
        images = []
        for i in range(4):
            for j in range(3):
                #get the idle image
                image = pg.Surface((16,16)).convert()
                image.blit(self.sheet, (0,0), ((j * 16),(i * 16), 16, 16))

                #REMOVE LATER
                #image = pg.transform.scale(image, (48, 48))


                images.append(image)

        return images