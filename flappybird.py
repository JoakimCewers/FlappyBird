from pydoc import cli
import pygame
import math
import random

pygame.init()

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
        self.alive = True

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
            if bird.alive == False:
                pipe.speed = -1
            pipe.checkColision(bird)
            pipe.drawPipe()

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
                bird.alive = False


    def changeHolePos(self):
        self.offest = random.randint(200,HEIGHT-200)

    def changeColor(self):
        self.color = (random.randint(200,255),random.randint(0,255),random.randint(0,255))

def drawWindow():
    WIN.fill(CYAN)

def draw_text(text,font,size,color,surface,x,y):
    fontObj = pygame.font.SysFont(font,size)
    textObj = fontObj.render(text,True,color)
    surface.blit(textObj,(x,y))

def randomColor():
    color = ((random.randint(200,255),random.randint(200,255),random.randint(200,255)))
    return color

def mousePos():
    pos = pygame.mouse.get_pos()
    return pos


def mainMenu():
    clock = pygame.time.Clock()
    run = True
    click = False
    while run:
        clock.tick(FPS)
        WIN.fill((CYAN))                                                # background color
        draw_text('Main menu','Corbel',60,BLACK,WIN,WIDTH/2-190,100)    # menu text

        gameButton = pygame.Rect(WIDTH/2-200,HEIGHT/2-100,300,100)         # created a rectangle
        pygame.draw.rect(WIN,WHITE,gameButton)                          # draws rect
        draw_text('Play','Corbel',60,BLACK,WIN,WIDTH/2-100,HEIGHT/2-75)
        
        if gameButton.collidepoint(mousePos()): # if mouse is on button
            if click:
                gameLoop()
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        pygame.display.update()
    pygame.quit()

def gameLoop(): # main game loop
   
    player = Bird(100,HEIGHT/2) # initialise the player and pipes
    collection = PipeCollection()

    for i in range(PIPEAMOUNT): # adds amount of pipes
        pipe = Pipes(WIDTH-i*WIDTH/PIPEAMOUNT)
        collection.addPipe(pipe)

    clock = pygame.time.Clock()     #starts clock
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.MOUSEBUTTONDOWN:    #if mouse clicked
                if player.alive:
                    player.vel = -4

            
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        
        if player.alive == False:   # go to death menu
            pass
        drawWindow()
        collection.update(player)
        player.draw()
        pygame.display.update()
        
    


if __name__ == "__main__":
    
    mainMenu()