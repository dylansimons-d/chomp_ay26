
# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
print(type(screen))
clock = pygame.time.Clock()
running = True

leroy_surface = pygame.Surface((100,50))
leroy_color = [115, 64, 14]
leroy_surface.fill(leroy_color)
leroy_x = 300
leroy_y = 200

sky_blue = [0, 150, 255]


leroy_speed = 2


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update YOUR PLAYERS #########################################
    leroy_x += leroy_speed

    if leroy_x >= 0.9 * WIDTH or leroy_x <=0:
        leroy_speed *= -1
        

   

    # draw
    screen.blit(leroy_surface, (leroy_x, 200))

    
    # RENDER YOUR GAME HERE ########################################
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(sky_blue)
    
    # blit leroy on the screen
    screen.blit(leroy_surface, (leroy_x, leroy_y))
    


    #################################################################

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()