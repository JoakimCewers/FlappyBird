from audioop import reverse
from ensurepip import bootstrap
from pydoc import cli
from turtle import distance
import pygame
import math
import random
from geneticNet import Organism,Ecosystem
import numpy as np

pygame.init()

WIDTH,HEIGHT = 1800,1000    
RADIUS = 50
FPS = 120
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (0,0,255)
CYAN=(0,255,255)
HOLEWIDTH = 200
PIPEAMOUNT = 3
img_player = pygame.image.load('./images/Flappy.png')
img_pipe = pygame.image.load('./images/pipeimage.png')

class Bird():

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.vel = 0
        self.acc = +0.1
        self.radius = 18
        self.alive = True
        self.ai = None
        self.distance = 0
        self.show = True
    def draw(self):
        #pygame.draw.circle(WIN,BLACK,(self.x,self.y),self.radius)
        WIN.blit(img_player,(self.x-self.radius-57,self.y-self.radius-35))
        
    def updatePos(self):
        self.y += self.vel
        self.vel += self.acc
    
    def reset(self):
        self.x = 100
        self.y = HEIGHT/2
        self.vel = 0
        self.alive = True
        self.distance = 0

class Nets():
    def __init__(self,size) -> None:
        self.collection = []
        self.size = self.innitNet(size)

    def innitNet(self,size):
        for i in range(size):
            bird = Bird(100,HEIGHT/2)
            bird.ai = Organism([2,4,4,2],output='softmax')
            bird.ai.mutate()
            self.collection.append(bird)
    def update(self,pipeCollection):
        end = 0
        for bird in self.collection:
            if bird.alive:
                bird.distance += 1
                prediction = predict(bird,pipeCollection)
                
                if prediction[0][0] < prediction[0][1]:
                    bird.vel = -4
                bird.updatePos()
                end +=1
                if bird.show:
                    bird.draw()
        if end == 0:
            return 1
        else: 
            return 0
def predict(bird,pipeCollection):
    pipes = pipeCollection.collection
    pipes.sort(key=lambda x: x.x)
    closestPipe = pipes[0]
    if closestPipe.x - bird.x < 0:
        closestPipe = pipes[1]

    distanceToPipe = closestPipe.x - bird.x
    normDTP = distanceToPipe/700
    if normDTP > 1:
        normDTP = 1
    distanceToHole = closestPipe.holepos - bird.y + HEIGHT/2
    normDTH = distanceToHole/HEIGHT
    X = np.array([[normDTH,normDTP]])
    print(X)
    return bird.ai.predict(X)

class PipeCollection():

    def __init__(self) -> None:
        self.collection = []
        

    def update(self,birds):
        for pipe in self.collection:

            #pipe.speed = -1
            pipe.checkColision(birds)
            pipe.drawPipe()

    def addPipe(self,newPipe):
        self.collection.append(newPipe)

        
class Pipe():

    def __init__(self,x) -> None:
        self.holepos = 0
        self.x = x
        self.width = 100
        self.color = BLACK
        self.speed = 5
        self.changeHolePos()
        self.changeColor()

    def drawPipe(self):
        self.movePipe()
        pygame.draw.rect(WIN,self.color,(self.x,0,self.width,self.holepos-HOLEWIDTH/2))
        pygame.draw.rect(WIN,self.color,(self.x,self.holepos+HOLEWIDTH/2,self.width,HEIGHT))
        #WIN.blit(img_pipe,(self.x,0,self.width,self.holepos-HOLEWIDTH/2))
        #WIN.blit(img_pipe,(self.x,self.holepos+HOLEWIDTH/2,self.width,HEIGHT))
        
    def movePipe(self):
        self.x -= self.speed
        if self.x < 0 - self.width:
            self.x = WIDTH
            self.changeHolePos()
            self.changeColor()

    def checkColision(self,birds):
        for bird in birds:
            if bird.x >= self.x and bird.x <= self.x + self.width:
            
                if bird.y - bird.radius <= self.holepos-HOLEWIDTH/2 or bird.y + bird.radius >= self.holepos+HOLEWIDTH/2:
                    #print(" U DEAD")
                    bird.alive = False
            if bird.y < 0 or bird.y > HEIGHT:
                bird.alive = False

    def changeHolePos(self):
        self.holepos += 200
        if self.holepos > HEIGHT-200:
            self.holepos = 200
        #self.holepos = random.randint(200,HEIGHT-200)

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

def updateScore(bird,pipeCollection):
    for pipe in pipeCollection.collection:
        if pipe.x == (bird.x - bird.radius+3):
            return 1
    return 0
            
def mainMenu():
    clock = pygame.time.Clock()
    run = True
    click = False
    returnButton = False
    high_score = 0
    bots = Nets(20)
    while run:
        clock.tick(FPS)
        WIN.fill((CYAN))                                                # background color
        draw_text('Main menu','Corbel',60,BLACK,WIN,WIDTH/2-190,100)    # menu text
        gameButton = pygame.Rect(WIDTH/2-200,HEIGHT/2-100,300,100)         # created a rectangle

        gameButton2 = pygame.Rect(WIDTH/2-200,HEIGHT/2+35,300,100) 

        pygame.draw.rect(WIN,WHITE,gameButton)                   # draws rect
        pygame.draw.rect(WIN,WHITE,gameButton2)    
        draw_text('Play','Corbel',60,BLACK,WIN,WIDTH/2-100,HEIGHT/2-75)
        draw_text('Play Ai','Corbel',60,BLACK,WIN,WIDTH/2-130,HEIGHT/2+50)
        draw_text('High score = ' + str(high_score),'Corbel',60,BLACK,WIN,WIDTH/2-200,HEIGHT/2+150)
        if gameButton.collidepoint(mousePos()) or returnButton:# if mouse is on button or enter button
            returnButton = False
            if click:
                click = False
                score = gameLoop(bots)
                if score > high_score:
                    high_score = score
                    print(high_score)

        if gameButton2.collidepoint(mousePos()):# if mouse is on button or enter button
            if click:
                click = False
                gameLoop(bots)
                bots.collection.sort(key=lambda x: x.distance,reverse=True)
                best = bots.collection[0]
                
                bots.collection[0].show = True
                for bird in bots.collection[1:]:
                    #bird.show = False
                    
                    if bird.distance < best.distance:
                        bird.ai.layers = best.ai.layers
                        bird.ai.biases = best.ai.biases
                    bird.ai.mutate(stdev=0.3)
                    bird.reset()
                bots.collection[0].reset()
                

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    run = False
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    
                if event.key == pygame.K_RETURN:
                    click = True
                    returnButton = True
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
        pygame.display.update()
    pygame.quit()

def gameLoop(bots): # main game loop
   
    player = Bird(100,HEIGHT/2) # initialise the player and pipes
    collection = PipeCollection()
    score = 0
    for i in range(PIPEAMOUNT): # adds amount of pipes
        pipe = Pipe( WIDTH /2 + i*WIDTH/PIPEAMOUNT)
        collection.addPipe(pipe)

    clock = pygame.time.Clock()#starts clock
    
    run = True
    while run:
        clock.tick(FPS)

        ## checks all pygame actions (for the player movement)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:    #if mouse clicked
                if player.alive:
                    player.vel = -4
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.alive:
                        player.vel = -4
                if event.key == pygame.K_ESCAPE:
                    run = False
        if player.alive == False:   # go to death menu (not impelented)
            return score
        else:
            score += updateScore(player,collection)
        drawWindow()
        collection.update(bots.collection)
        end = bots.update(collection)
        if end:
            return
        #draw_text('Score = ' + str(score),'Corbel',60,BLACK,WIN,WIDTH/2-200,HEIGHT/2+150)
        pygame.display.update()
        
        
if __name__ == "__main__":
    
    mainMenu()