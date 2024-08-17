import pygame

pygame.init()

screen = pygame.display.set_mode((1000,800))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    clock.tick(60)

pygame.quit()