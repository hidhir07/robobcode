import pygame
from time import sleep
# Variables
# xC and yC are Current x and y coordinates of the Robob.
# xF and yF are Final x and y coordinates of the Robob(point to go to).
# xP and yP are the x and y Paths the Robob has to take (Robob travels in taxicab distances).
# xD and yD are the directions which the Robob is facing

# Functions
# MoveTo(xF,yF):
#   Recursive function to move one grid. Calls itself to move to the next grid.
# Forward():
#   Moves forward by exactly one grid.
# Right():
#   Turns right.
# Left():
#   Turns left.
debugging = True
xD, yD = 1, 0
xC, yC = 0, 0
gX, gY = 0,0
def Forward():
    global xD
    global yD
    global xC
    global yC
    if (debugging):
        print("Forward")
    xC += xD
    yC += yD
    
def Right():
    global xD
    global yD
    if (debugging):
        print("Right")
    if (xD==1):
        xD=0
        yD=1
    elif (yD==1):
        yD=0
        xD=-1
    elif (xD==-1):
        xD=0
        yD=-1
    elif (yD==-1):
        yD=0
        xD=1

def Left():
    global xD
    global yD
    if (debugging):
        print("Left")
    if (xD==1):
        xD=0
        yD=-1
    elif (yD==1):
        yD=0
        xD=1
    elif (xD==-1):
        xD=0
        yD=1
    elif (yD==-1):
        yD=0
        xD=-1
        


def MoveTo(xF,yF):
    global xC
    global yC
    global xD
    global yD

    FreshScreen()
    DrawArrow(xC,yC,xD,yD,(255,0,0))
    pygame.display.flip()
    
    # Calculate path
    xP, yP = xF-xC, yF-yC

    #                P
    #           -c   0   c  
    #       -1   c   0  -c
    #   D    0   0   0   0
    #        1  -c   0   c
    #
    
    # Generate case
    case = ""

    case += "X"
    case += "T" if (xP*xD>0) else "F"
    case += "0" if (xP == 0) else "C"

    case += "Y"
    case += "T" if (yP*yD>0) else "F"
    case += "0" if (yP == 0) else "C"
    
    # Run through cases
    if (debugging):
        print("[DEBUG] {}".format(case))
    if (case in ["XTCYFC","XF0YTC","XFCYTC","XTCYF0"]):
        Forward()
    elif (case in ["XF0YFC"]):
        if ((xD==1 and yP<0)or(xD==-1 and yP>0)):
            Left()
        elif ((xD==1 and yP>0)or(xD==-1 and yP<0)):
            Right()
        else:
            Right()
    elif (case in ["XFCYF0"]):
        if ((yD==1 and xP>0)or(yD==-1 and xP<0)):
            Left()
        elif ((yD==1 and xP<0)or(yD==-1 and xP>0)):
            Right()
        else:
            Right()
    elif (case in ["XFCYFC"]):
        if ((xD==1 and yP<0)or(xD==-1 and yP>0)or(yD==1 and xP>0)or(yD==-1 and xP<0)):
            Left()
        elif ((xD==1 and yP>0)or(xD==-1 and yP<0)or(yD==1 and xP<0)or(yD==-1 and xP>0)):
            Right()
        else:
            Right()
    if (debugging):
        print("[Debug] Current Location: {},{}\n[Debug] Current Direction: {},{}".format(xC,yC, xD,yD))
    

    sleep(0.5)
    if(case not in ["XF0YF0"]):
        MoveTo(xF,yF)
    else:
        FreshScreen()
        DrawArrow(xC,yC,xD,yD,(0,255,0))
        pygame.display.flip()
        
def FreshScreen():
    global gX, gY
    
    screen.fill(bgColor)
    pygame.draw.rect(screen,(255,255,0),(gX*50,gY*50,50,50),0)
    for i in range(0,401,50):
        pygame.draw.rect(screen, (0,0,0), [i,0,1,550], 1)
    for i in range(0,551,50):
        pygame.draw.rect(screen, (0,0,0), [0,i,400,1], 1)
    
    pygame.display.flip()

def DrawArrow(xC,yC,xD,yD,color):
    if (xD==1):
        pygame.draw.polygon(screen, color, [(3+xC*50,23+yC*50),
                                             (26+xC*50,23+yC*50),
                                             (26+xC*50,15+yC*50),
                                             (46+xC*50,25+yC*50),
                                             (46+xC*50,26+yC*50),
                                             (26+xC*50,36+yC*50),
                                             (26+xC*50,28+yC*50),
                                             (3+xC*50,28+yC*50)],0)
    elif (yD==1):
        pygame.draw.polygon(screen, color, [(21+xC*50,3+yC*50),
                                             (26+xC*50,3+yC*50),
                                             (26+xC*50,26+yC*50),
                                             (34+xC*50,26+yC*50),
                                             (24+xC*50,46+yC*50),
                                             (23+xC*50,46+yC*50),
                                             (13+xC*50,26+yC*50),
                                             (21+xC*50,26+yC*50)],0)
    elif (xD==-1):
        pygame.draw.polygon(screen, color, [(3+xC*50,24+yC*50),
                                             (3+xC*50,23+yC*50),
                                             (23+xC*50,13+yC*50),
                                             (23+xC*50,21+yC*50),
                                             (46+xC*50,21+yC*50),
                                             (46+xC*50,26+yC*50),
                                             (23+xC*50,26+yC*50),
                                             (23+xC*50,34+yC*50)],0)
    elif (yD==-1):
        pygame.draw.polygon(screen, color, [(15+xC*50,23+yC*50),
                                             (25+xC*50,3+yC*50),
                                             (26+xC*50,3+yC*50),
                                             (36+xC*50,23+yC*50),
                                             (28+xC*50,23+yC*50),
                                             (28+xC*50,46+yC*50),
                                             (23+xC*50,46+yC*50),
                                             (23+xC*50,23+yC*50)],0)
    


    
bgColor = (255,255,255)
screenSize = (400,550)
screen = pygame.display.set_mode(screenSize)
FreshScreen()
DrawArrow(xC,yC,xD,yD,(0,255,0))
pygame.display.flip()

while True:
    ev = pygame.event.get()
    # proceed events
    for event in ev:
        # handle MOUSEBUTTONUP
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            gX = int(pos[0]/50)
            gY = int(pos[1]/50)
            pygame.draw.rect(screen,(255,0,0),(gX*50,gY*50,50,50),0)
            MoveTo(gX,gY)
    sleep(0.1)
















    
