# Sample pygame code for CS111 final Project
# Author: Sherri Goings
# Last modified: 3/5/2013

import pygame
from random import *

def getRandColor():
    """ returns an rgb tuple with random values between 0 and 255 """
    return (randrange(0,256), randrange(0,256), randrange(0,256))

class targetPractice:
    """ overall game class """
    
    def __init__(self, numBoxes, winWidth, winHeight):
        """ game constructor. Takes arguments:
              number of target boxes,
              width of game window,
              height of game window
        initializes crossHairs and given number of target boxes with random parameters """

        self.cross = crossHairs(50, (100,0,50), (winWidth/2, winHeight/2), (0, winWidth), (0, winHeight))
        self.crossMoving = False

        self.numBoxes = numBoxes
        self.boxes = []
        # initialize boxes with different colors, sizes, speeds, and start positions but all allowed to
        # bounce around anywhere in the window (same bounds)
        for i in range(numBoxes):
            size = randrange(20,50)
            color = getRandColor()
            pos = (randrange(0,winWidth-size), randrange(0,winHeight-size))
            speed = (randrange(1,4))
            newBox = movingBox(size, color, pos, speed, (0, winWidth), (0, winHeight))
            self.boxes.append(newBox)

    def handleEvent(self, event):
        """ checks for left mouse button press/release, mouse motion, and spacebar press and takes
        appropriate action for each """
        
        # if user presses space when crosshairs are inside a box, change its color to a random new color
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            crossPos = self.cross.getPos()
            for box in self.boxes:
                boxPos = box.getPos()
                boxSide = box.getSideLength()
                if (boxPos[0] < crossPos[0] < boxPos[0]+boxSide) and (boxPos[1] < crossPos[1] < boxPos[1]+boxSide):
                    box.changeColor()

        # if user presses the left mouse button, set moving to True, so the crosshairs
        # will now follow the mouse
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.crossMoving = True

        # if user releases the left mouse button, set moving to False, so the crosshairs will
        # stop following the mouse
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.crossMoving = False

        # if the mouse moves, and moving is true (which because of the above 2 statements means
        # the left mouse button is being held down), get the position of the mouse
        if event.type == pygame.MOUSEMOTION and self.crossMoving:
            self.cross.updatePos(event.pos)

    def draw(self, screen):
        """ draws the crosshairs and all boxes """
        self.cross.draw(screen)
        for box in self.boxes:
            box.draw(screen)
            
    def moveTargets(self):
        """ moves all of the target boxes 1 step """
        for box in self.boxes:
            box.moveStep()

    
class movingBox:
    """ class that represents a simple square that can move around the screen """
    def __init__(self, sideLength, color, initPos, speed, boundsX, boundsY):
        """ movingBox constructor. Takes arguments:
              length of side of the square box
              color to fill the box
              tuple or list with x,y coordinates of initial position
              speed at which box will move (how many pixels per step)
              tuple or list with min,max allowed x coordinates for the box to occupy
              tuple or list with min,max allowed y coordinates for the box to occupy """
        
        self.sideLength = sideLength
        self.pos = list(initPos)
        self.color = color
        self.speed = speed
        self.dir = [1,1]
        self.boundsX = boundsX
        self.boundsY = boundsY

    def draw(self, screen):
        """ draws the box to the screen """
        pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.sideLength, self.sideLength))

    def moveStep(self):
        """ moves the box one step in its current direction, unless it hits a wall in which case
        it changes the current direction """
        if self.pos[0] <= self.boundsX[0] or (self.pos[0]+self.sideLength) >= self.boundsX[1]:
            self.dir[0] *= -1
        if self.pos[1] <= self.boundsY[0] or (self.pos[1]+self.sideLength) >= self.boundsY[1]:
            self.dir[1] *= -1
            
        self.pos[0] += self.dir[0]*self.speed
        self.pos[1] += self.dir[1]*self.speed

    def getSideLength(self):
        return self.sideLength

    def getPos(self):
        return self.pos

    def changeColor(self):
        self.color = getRandColor()
       

class crossHairs:
    """ class to represent the crosshairs of a gun """
    def __init__(self, length, color, initPos, boundsX, boundsY):
        """ crossHairs constructor. Takes arguments:
              radius of crosshairs 
              color to draw crosshairs
              tuple or list with x,y coordinates of initial position
              tuple or list with min,max allowed x coordinates for the box to occupy
              tuple or list with min,max allowed y coordinates for the box to occupy """

        self.length = length
        self.color = color
        self.pos = list(initPos)
        self.moving = False
        self.boundsX = boundsX
        self.boundsY = boundsY
        
    def draw(self, screen):
        """ draw crosshairs with 2 lines """
        pygame.draw.line(screen, self.color, (self.pos[0]-50,self.pos[1]),(self.pos[0]+50,self.pos[1]))
        pygame.draw.line(screen, self.color, (self.pos[0],self.pos[1]-50),(self.pos[0],self.pos[1]+50))
        
    def updatePos(self, mouse):
        """ move crosshairs position to the position of the given mouse coordinates """
        if mouse[0] > (self.boundsX[0]+self.length) and mouse[0] < (self.boundsX[1]-self.length):
            self.pos[0] = mouse[0]
        if mouse[1] > (self.boundsY[0]+self.length) and mouse[1] < (self.boundsY[1]-self.length):
            self.pos[1] = mouse[1]

    def getPos(self):
        return self.pos

                
def main():
    """ plays targetPractice game """

    # sets up all pygame modules for use
    pygame.init()
    
    # set up window with given width, height, and caption
    winWidth, winHeight = 640, 600
    screen = pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("Exploring mouse, keys, and event loops with Pygame")

    # initialize parameters and draw just background screen
    running = 1
    bgcolor = (100,100,250)
    screen.fill(bgcolor)

    # create a new targetPractice game with 5 targets and draw initial game screen
    game = targetPractice(5, winWidth, winHeight)
    game.draw(screen)
    
    # add text box
    myfont = pygame.font.SysFont("Cambria", 22)
    instsLine1 = myfont.render("Instructions: Hold down the left mouse button while sliding", 1, (75, 0, 75))
    instsLine2 = myfont.render("the mouse to move the crosshairs. Press the space bar with", 1, (75, 0, 75))
    instsLine3 = myfont.render("the cross hairs inside of a square to change the color.", 1, (75, 0, 75))
    myfont = pygame.font.SysFont("Cambria", 28)
    instsLine4 = myfont.render("                      PRESS RETURN TO BEGIN", 1, (75, 0, 75))
    screen.blit(instsLine1, (50, 100))
    screen.blit(instsLine2, (50, 125))
    screen.blit(instsLine3, (50, 150))
    screen.blit(instsLine4, (50, 180))
    pygame.display.flip()

    # create the graphics clock
    clock = pygame.time.Clock()

    # continuously poll to see if the user has pressed the return key (an event has occurred of
    # the type KEYDOWN means some key was pressed, so then check the specific event.key to see if
    # it was the RETURN key.
    event = pygame.event.poll()
    while not (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
        clock.tick(50)
        event = pygame.event.poll()
        

    # Now continue until user clicks x to close window
    while event.type != pygame.QUIT:
        
        # start by "erasing" everything currently drawn by painting screen with background color
        screen.fill(bgcolor)

        # see if any event has happened and if so take the appropriate action
        game.handleEvent(event)

        # move the target boxes one step each
        game.moveTargets()

        # draw the boxes and crosshairs at the appropriate current positions
        game.draw(screen)

        # show the new screen drawn
        pygame.display.flip()

        # keeps pygame from using all of comp's cpu (works a bit like sleep, except here a bigger
        # number means a shorter wait, think of the parameter more as speed, values between
        # 20 and 100 seem to be reasonable, depending on how fast you want things to move)
        clock.tick(50)

        # get next event
        event = pygame.event.poll()

if __name__=="__main__":
    main()
