import pygame
import math
import random
#pygame.init()

WIDTH,HEIGHT = 1800,1000
RADIUS = 50
FPS = 120
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)




class Bird():

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.vel = 0
        self.accel = 0

    def draw(self):
        
        pygame.draw.circle(WIN,BLACK,(self.x,self.y),20)
    

def drawWindow(player = Bird):
    WIN.fill((255,255,255))
    player.draw()
    pygame.display.update()
    
def main():
    
    player = Bird(100,HEIGHT/2)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

            if event.type == pygame.QUIT:
                run = False

        drawWindow(player)
        
        
    pygame.quit()

def mousePos():
    pos = pygame.mouse.get_pos()
    return pos





if __name__ == "__main__":
    
    main()