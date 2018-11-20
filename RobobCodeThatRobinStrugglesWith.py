# Run in Python 3
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
from flask import Flask, request, abort
import json

import RPi.GPIO as GPIO
from time import sleep
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
Motor1A = 16
Motor1B = 18
Motor1E = 22

Motor2A = 23
Motor2B = 21
Motor2E = 19

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2E, GPIO.OUT)



debugging = True
xD, yD = 1, 0
xC, yC = 0, 0


pwm1 = GPIO.PWM(Motor1E,100)
pwm2 = GPIO.PWM(Motor2E,100)

pwm1.start(0)
pwm2.start(0)

pwm1.ChangeDutyCycle(65)
pwm2.ChangeDutyCycle(65)


def Forward():
    global xD
    global yD
    global xC
    global yC
    if (debugging):
        print("Forward")
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)  
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.LOW)
    GPIO.output(Motor2E, GPIO.LOW)
    sleep(0.26)
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
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(0.55)

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

    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)
    sleep(0.55)


def MoveTo(xF,yF):
    global xC
    global yC
    global xD
    global yD
    
    # Read current position
    robobxy = open("coords.eatnow","r")
    coords = robobxy.read().split(",")
    robobxy.close()

    # Get current position
    xC, yC = int(coords[0]), int(coords[1])

    # Calculate path
    xP, yP = int(xF)-xC, int(yF)-yC

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
    if (debugging):
        print("[DEBUG] {}".format(case))
    # Run through cases

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
        elif ((yD==1 and xP<0)or(yD==-1 and xp>0)):
            Right()
        else:
            Right()
    elif (case in ["XFCYFC"]):
        if ((xD==1 and yP<0)or(xD==-1 and yP>0)or(yD==1 and xp>0)or(yD==-1 and xP<0)):
            Left()
        elif ((xD==1 and yP>0)or(xD==-1 and yP<0)or(yD==1 and xP<0)or(yD==-1 and xP>0)):
            Right()
        else:
            Right()
    if (debugging):
        print("[Debug] Current Location: {},{}\n[Debug] Current Direction: {},{}".format(xC,yC, xD,yD))
    if(case not in ["XT0Yf0","XF0YT0"]):
        MoveTo(xF,yF)
    else:
        print("Woohoo")
        GPIO.output(Motor1E, GPIO.LOW)
        GPIO.output(Motor2E, GPIO.LOW)

# Flask- receives HTTP requests
app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
	# Called once the pi receives a request
	x = request.form['x']
	y = request.form['y']
	MoveTo(x,y)
	return 'all gud c:'

if __name__ == '__main__':
	app.run(host='0.0.0.0')















    
