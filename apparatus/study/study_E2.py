import sys
from sys import argv
import datetime
import time
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import os
import logging
from shutil import copyfile
import configparser

config = configparser.ConfigParser()
config.read('/home/pi/Documents/stickPull/config')

filename_temp =  datetime.datetime.now().strftime("%m.%d.%Y_%H:%M:%S") + '_Enclosure2_study_logfile.log' 
log_path_temp = 'logfiles/'
Enclosre_nr = config['ENCLOSURE']['ID']
dest_log_path = '/mnt/piwebcam/Log files stick pulling/Enclosure'+Enclosre_nr+'/study/' + filename_temp

logging.basicConfig(filename = log_path_temp+filename_temp,format='%(asctime)s %(message)s', level = logging.INFO)

logging.info('*********** PROGRAM START **********')


pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

DIR_R = int(config['PIN_BRUSH']['DIR_R'])
PUL_R = int(config['PIN_BRUSH']['PUL_R'])
DIR_L = int(config['PIN_BRUSH']['DIR_L'])
PUL_L = int(config['PIN_BRUSH']['PUL_L'])
ENA_L = int(config['PIN_BRUSH']['ENA_L'])
ENA_R = int(config['PIN_BRUSH']['ENA_R'])
ID_L = int(config['IDMOTOR']['ID_L'])
ID_R = int(config['IDMOTOR']['ID_R'])
ID_oat_R = int(config['IDMOTOR']['ID_oat_R'])
ID_oat_L = int(config['IDMOTOR']['ID_oat_L'])

runningMode = ''
feedingside = ''

rat_start_time = 0
ratAte = False
b_changeMode = False
leftSide = False
rightSide = False
prg_start = 0
b_start = False
sideJustPulled = False
ex_time = 0
timestamp_pulls_L = []
timestamp_pulls_R = []

closed_L = int(config['MOTORPOS']['closed_L'])
open_L_free = int(config['MOTORPOS']['free_L'])
open_R_free = int(config['MOTORPOS']['free_R'])
closed_R = int(config['MOTORPOS']['closed_R'])
open_L = int(config['MOTORPOS']['open_L'])
open_R = int(config['MOTORPOS']['open_R'])
feed_L_back = int(config['MOTORPOS']['feed_L_back'])
feed_L_front = int(config['MOTORPOS']['feed_L_front'])
feed_R_back = int(config['MOTORPOS']['feed_R_back'])
feed_R_front = int(config['MOTORPOS']['feed_R_front'])
oat_open_L = int(config['MOTORPOS']['oat_open_L'])
oat_open_R = int(config['MOTORPOS']['oat_open_R'])
oat_close_L = int(config['MOTORPOS']['oat_close_L'])
oat_close_R  = int(config['MOTORPOS']['oat_close_R'])


##### SETUP PINS #####
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_R, GPIO.OUT)
GPIO.setup(PUL_R, GPIO.OUT)
GPIO.setup(ENA_R, GPIO.OUT)

GPIO.setup(DIR_L, GPIO.OUT)
GPIO.setup(PUL_L, GPIO.OUT)
GPIO.setup(ENA_L, GPIO.OUT)

#### MOTOR FUNCTIONS ####

def move_mot(nr, targetPos):
    pwm.set_pwm(int(nr),0, int(targetPos))
    print("move motor " + str(nr)+ " to : "+ str(targetPos))
    logging.info("move motor " + str(nr)+ " to : "+ str(targetPos))
    time.sleep(1)
    pwm.set_pwm(int(nr),0, int(0))
    
def turn_brush(DIR, PUL, b_side, st_dl = 0.000005):
    GPIO.output(DIR, b_side)
    GPIO.output(PUL, False)
    for i in range(1530):
	GPIO.output(PUL, True)
	time.sleep(st_dl)
	GPIO.output(PUL, False)
	time.sleep(st_dl)

def move_brush(DIR, PUL, ENA):
    GPIO.output(ENA, True)
    # turn_brush(DIR, PUL, True)
    turn_brush(DIR, PUL, False)
    GPIO.output(ENA, False)

def release_oat(side = ''):
    if (side == 'R')| (side==''):
	move_mot(ID_oat_R, oat_open_R)
	move_brush(DIR_R, PUL_R, ENA_R)
	move_mot(ID_oat_R, oat_close_R)
	pwm.set_pwm(ID_oat_R,0,0)
    	print("release oat on right side from close: "+ str(oat_close_R) +" to open:"+ str(oat_open_R))
    	logging.info('release oat on right side ')
    if (side == 'L') | (side==''):
	move_mot(ID_oat_L, oat_open_L)
	move_brush(DIR_L, PUL_L, ENA_L)
	move_mot(ID_oat_L, oat_close_L)
	pwm.set_pwm(ID_oat_L,0,0)
    	print("release oat on right side from close: "+ str(oat_close_L) +" to open:"+ str(oat_open_L))
    	logging.info('release oat on left side ')


print("close both motors")
move_mot(ID_L, closed_L)
move_mot(ID_R, closed_R)
release_oat('R')
release_oat('L')
sideJustPulled = False
rightSide = False
leftSide = False
move_mot(ID_L, open_L)
move_mot(ID_R, open_R)
move_mot(ID_L, open_L_free)
#***** BUTTONS *****
button_R2 = int(config['PIN_BUTTON']['R2']) # config.buttons["button_R1"] L2
button_R1 = int(config['PIN_BUTTON']['R1'])
button_L1 = int(config['PIN_BUTTON']['L1'])
button_L2 = int(config['PIN_BUTTON']['L2'])

rat_start_time = 0

try:
    rat_eating_time = float(sys.argv[2])
    print("rat eating time: " + str(rat_eating_time)+ " sec")
except:
    print("The eating time will be 10 sec")

ex_time = float(sys.argv[1])
print("program will run for " + str(ex_time)+" min")

R1 = True
R2 = False
L1 = True
L2 = False

def callback_R1(self):
    global R1, R2
    logging.info('R1 was pressed ')
    print("R1 was pressed ")
    R1 = True
    R2 = False

def callback_R2(self):
    global  sideJustPulled, rightSide, leftSide, R1, R2
    if not(sideJustPulled) and not(leftSide):
	move_mot(ID_L, closed_L)
	sideJustPulled = True
	rightSide = True
	leftSide = False
	logging.info('rat pulled on left side ')
        print("rat pulled on left side")
	timestamp_pulls_R.append(datetime.datetime.now())
    logging.info('R2 was pressed ')
    R1 = False
    R2 = True
    print("R2 was pressed")

def callback_L1(self):
    global L1, L2
    logging.info('L1 was pressed ')
    print("L1 was pressed ")    
    L1 = True
    L2 = False

def callback_L2(self):
    global sideJustPulled, leftSide, L1, L2
    if not(sideJustPulled) and not(rightSide):
	move_mot(ID_R, closed_R)
	sideJustPulled = True
	leftSide = True
	logging.info('rat pulled on right side ')
	timestamp_pulls_L.append(datetime.datetime.now())
	print("rat pulled on right side")
    L1 = False
    L2 = True
    logging.info('L2 was pressed ')
    print("L2 was pressed")
    


GPIO.setup(button_R1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_R2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_L1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_L2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(button_R1, GPIO.FALLING, bouncetime=300)
GPIO.add_event_callback(button_R1, callback_R1)
GPIO.add_event_detect(button_R2, GPIO.FALLING, bouncetime=300)
GPIO.add_event_callback(button_R2, callback_R2)
GPIO.add_event_detect(button_L1, GPIO.FALLING, bouncetime=300)
GPIO.add_event_callback(button_L1, callback_L1)
GPIO.add_event_detect(button_L2, GPIO.FALLING, bouncetime=300)
GPIO.add_event_callback(button_L2, callback_L2)

notChanged = True
last_print = 0
diff = 0
needs_refill = True
b_start = True # start the program

rat_is_eating = False
update_rat_start_time = False
'''
if not(GPIO.input(button_R1)):
		print("button R1 is pressed")
	if not(GPIO.input(button_L1)):
		print("button L1 is pressed")
'''

    

pull_back_timer = datetime.datetime.now()
def rat_eats():
    global ratAte, update_rat_start_time, rat_start_time
    print("rat is eating, update_rat_start_time: "+ str(update_rat_start_time)+ " rat start time: "+ str(rat_start_time))
    if update_rat_start_time:
	print("timediff of eating rat: "+ str((datetime.datetime.now()- rat_start_time).total_seconds))
	print(((datetime.datetime.now()- rat_start_time).total_seconds() > (rat_eating_time)))
	print(rat_eating_time)
	if ((datetime.datetime.now()- rat_start_time).total_seconds() > (rat_eating_time)):
	    print("rat ate")
	    logging.info('rat ate')
	    ratAte = True
	    update_rat_start_time = False
    else:
	# print("rat eating time is updatet")
	rat_start_time = datetime.datetime.now()
	update_rat_start_time = True
lastPrint = datetime.datetime.now()


def smloop():
    global lastPrint,diff, ratAte, feedingSide, leftSide, rightSide, sideJustPulled, pull_back_timer
    # print("hey ")
    # lastPrint = datetime.datetime.now()
    # static variable with writer
    # write function to write 
    # write row only at some time
    # append et apres ecris par ligne et le faire
    
    currentTime  = datetime.datetime.now()
    diff = currentTime - lastPrint
    lastPrint = currentTime
    # print(diff.total_seconds())
    
    # if ((datetime.datetime.now()-lastPrint).total_seconds() > 3):
	# lastPrint = datetime.datetime.now()
    
    print("side just pulled: "+str(sideJustPulled)+", left side: " + str(leftSide) + ", right side: "+ str(rightSide) + ", rat ate: "+ str(ratAte))
    if sideJustPulled:
	if not(ratAte):
	    if rightSide:
		if ratAte:
		    print("right side pulled, rat eating right side")
		else:
		    rat_eats()
		    if not(L1):
			move_mot(ID_L, closed_L)
		    else:
			move_mot(ID_L, 0)
	    if leftSide:
		if ratAte:
		    print("left side pulled, rat eating left side")
		else:
		    rat_eats()
		    if not(R1):
			move_mot(ID_R, closed_R)
		    else:
			move_mot(ID_R, 0)
	elif (rightSide and (GPIO.input(button_R1))) or (leftSide and (GPIO.input(button_L1))):
	    if rightSide:
		if (datetime.datetime.now() - pull_back_timer).total_seconds()> 3:
		    print("right side pulled, rat ate on right side")
		    logging.info('try pull motor back on right ')
		    print('try pull motor on right side')
		    pull_back_timer = datetime.datetime.now()
		    move_mot(ID_R, feed_R_front)
		    move_mot(ID_R,  feed_R_back)
	    if leftSide:
		print("side pulled, rat ate on left side")
		if (datetime.datetime.now() - pull_back_timer).total_seconds() > 3:
		    pull_back_timer = datetime.datetime.now()
		    move_mot(ID_L, feed_L_front)
		    move_mot(ID_L,  feed_L_back)
		    logging.info('try pull motor back on left ')
		    print('try pul motor on left side')
	elif ((rightSide and not(GPIO.input(button_R1)) ) or (leftSide and not(GPIO.input(button_L1)) ) and ratAte):
	    print("should release oat")
	    if rightSide:
		move_mot(ID_R, 0)
		release_oat('R')
		logging.info('release oat on right side ')
		print('release oat on right side')
	    else:
		move_mot(ID_L, 0)
		release_oat('L')		
		logging.info('release oat on left side ')
		print('release oat on left side')
	    rightSide = False
	    leftSide = False
	    sideJustPulled = False
	    ratAte = False
	    move_mot(ID_L,  open_L)
	    move_mot(ID_R,  open_R)
	    move_mot(ID_L, open_L_free)

run_prg = True
prg_start_time = datetime.datetime.now()
while (datetime.datetime.now()- prg_start_time).total_seconds()< (ex_time*60):
    smloop()
GPIO.cleanup()

move_mot(ID_R, closed_R)
move_mot(ID_L, closed_L)
move_mot(ID_R, closed_R)
move_mot(ID_L, closed_L)
move_mot(ID_R, closed_R)
move_mot(ID_L, closed_L)
'''
while not(GPIO.input(button_R1)) and not(GPIO.input(button_L1)):
    move_mot(ID_R, open_R)
    move_mot(ID_L, open_L)
    move_mot(ID_R,  closed_R)
    move_mot(ID_L,  closed_L)
move_mot(ID_R, 0)
move_mot(ID_L, 0)
'''
print('total pulls on right side: '+str(len(timestamp_pulls_L)) + ' total pulls on left side: '+ str(len(timestamp_pulls_R)))
logging.info('total pulls on right side: '+str(len(timestamp_pulls_L)) + ' total pulls on left side: '+ str(len(timestamp_pulls_R)))
print('timestamp pulls on right side:')
logging.info('timestamp pulls on right side:')
for i in timestamp_pulls_L:
    print(i)
    logging.info(i)
logging.info('timestamp pulls on left side:')
print('timestamp pulls on left side:')
for i in timestamp_pulls_R:
    print(i)
    logging.info(i)
print('PROGAM END')
logging.info('*********** PROGRAM END **********')
copyfile(log_path_temp+filename_temp, dest_log_path)
os.remove(log_path_temp)
