import Adafruit_PCA9685
import time
import RPi.GPIO as GPIO
import os

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

def move_mot(nr, angle):
	pwm.set_pwm(int(nr),0, int(angle))
	print("move motor"+ str(nr) + " to: "+ str(angle))
	time.sleep(0.5)
	pwm.set_pwm(int(nr),0,0)
	
global ID, curr_pos
ID = 0
curr_pos = 0
'''
def u():
	curr_pos = curr_pos +10
	move_mot(ID_mot, curr_pus)

def j():
	curr_pos = curr_pos -10
	move_mot(ID_mot, curr_pus)

def ID(id):
	print("ID: "+str(id))
	ID_mot = id

def start(st):
	print("start: "+str(st))
	curr_pos = st
	move_mot(ID_mot, st)
	'''

u = "up"
j = "down"
while True:
	a = input()
	try:
		(int(a))
		if a < 16:
			ID = int(a)
			print("set ID to "+str(a))
		else:
			curr_pos = a
			move_mot(ID, int(a))
	except:
		if a == u:
			curr_pos = curr_pos + 10
			move_mot(ID, curr_pos)
		if a == j:
			curr_pos = curr_pos - 10
			move_mot(ID, curr_pos)

