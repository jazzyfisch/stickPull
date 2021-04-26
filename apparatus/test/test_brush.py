
import RPi.GPIO as GPIO
import configparser
import time

config = configparser.ConfigParser()
config.read('/home/pi/Documents/stickPull/config.conf')
GPIO.setmode(GPIO.BCM)
DIR_R = int(config['PIN_BRUSH']['DIR_R'])
PUL_R = int(config['PIN_BRUSH']['PUL_R'])
DIR_L = int(config['PIN_BRUSH']['DIR_L'])
PUL_L = int(config['PIN_BRUSH']['PUL_L'])
ENA_L = int(config['PIN_BRUSH']['ENA_L'])
ENA_R = int(config['PIN_BRUSH']['ENA_R'])
st_dl = float(config['BRUSH']['st_dl'])
range_br = int(config['BRUSH']['range_br'])

GPIO.setup(DIR_R, GPIO.OUT)
GPIO.setup(PUL_R, GPIO.OUT)
GPIO.setup(DIR_L, GPIO.OUT)
GPIO.setup(PUL_L, GPIO.OUT)
GPIO.setup(ENA_L, GPIO.OUT)
GPIO.setup(ENA_R, GPIO.OUT)


r ='R'
l = 'L'

def turn(side):
	if side == "R":
		move_brush(DIR_R, PUL_R, ENA_R)
	else:
		move_brush(DIR_L, PUL_L, ENA_L)

def turn_brush(DIR, PUL, b_side, st_dl = st_dl):
    GPIO.output(DIR, b_side)
    GPIO.output(PUL, False)
    for i in range(range_br):
		GPIO.output(PUL, True)
		time.sleep(st_dl)
		GPIO.output(PUL, False)
		time.sleep(st_dl)

def move_brush(DIR, PUL, ENA):

    GPIO.output(ENA, True)
    # turn_brush(DIR, PUL, True)
    turn_brush(DIR, PUL, False)
    GPIO.output(ENA, False)


while True:
	a = input()
	turn(a)
