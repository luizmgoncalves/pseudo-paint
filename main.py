import pygame

pygame.init()

screen = pygame.display.set_mode((300, 300))

running = True

while running:
    screen.fill((255, 255, 255))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
