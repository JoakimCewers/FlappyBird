import pygame
import math
import random
#pygame.init()

WIDTH,HEIGHT = 1800,1000    
RADIUS = 50
FPS = 120
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)
WHITE = (255,255,255)
CYAN=(0,255,255)
HOLEWIDTH = 200
PIPEAMOUNT = 3

class Bird():

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.vel = 0
        self.acc = +0.1
        self.radius = 20

    def draw(self):
        self.updatePos()
        pygame.draw.circle(WIN,BLACK,(self.x,self.y),self.radius)

    def updatePos(self):
        
        self.y += self.vel
        self.vel += self.acc
        
    


class PipeCollection():

    def __init__(self) -> None:
        self.collection = []

    def update(self,bird):
        for pipe in self.collection:
            pipe.drawPipe()
            pipe.checkColision(bird)

    def addPipe(self,newPipe):
        self.collection.append(newPipe)

    def checkColision(self,bird):
        for pipe in self.collection:
            pipe.checkColision()
        


class Pipes():

    def __init__(self,x) -> None:
        self.offest = 0
        self.x = x
        self.width = 100
        self.color = BLACK
        self.speed = 5
        self.changeHolePos()
        self.changeColor()

    def drawPipe(self):
        self.movePipe()
        pygame.draw.rect(WIN,self.color,(self.x,0,self.width,self.offest-HOLEWIDTH/2))
        pygame.draw.rect(WIN,self.color,(self.x,self.offest+HOLEWIDTH/2,self.width,HEIGHT))
        
    def movePipe(self):
        self.x -= self.speed
        if self.x < 0 - self.width:
            self.x = WIDTH
            self.changeHolePos()
            self.changeColor()

    def checkColision(self,bird):

        if bird.x >= self.x and bird.x <= self.x + self.width:
        
            if bird.y - bird.radius <= self.offest-HOLEWIDTH/2 or bird.y + bird.radius >= self.offest+HOLEWIDTH/2:
                print(" U DEAD")


    def changeHolePos(self):
        self.offest = random.randint(200,HEIGHT-200)

    def changeColor(self):
        self.color = (random.randint(200,255),random.randint(0,255),random.randint(0,255))


def drawWindow():
    WIN.fill(CYAN)


    
def main():
    
    player = Bird(100,HEIGHT/2)
    collection = PipeCollection()

    for i in range(PIPEAMOUNT):
        pipe = Pipes(WIDTH-i*WIDTH/PIPEAMOUNT)
        collection.addPipe(pipe)

    #pipe = Pipes(WIDTH, random.randint(200,HEIGHT-200))
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.vel = -4

            if event.type == pygame.QUIT:
                run = False

        drawWindow()
        collection.update(player)
        
        player.draw()
        pygame.display.update()
        
        
        
    pygame.quit()

def mousePos():
    pos = pygame.mouse.get_pos()
    return pos



if __name__ == "__main__":
    
    main()