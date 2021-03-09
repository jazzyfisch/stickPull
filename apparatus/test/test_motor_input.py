import Adafruit_PCA9685
import time
import RPi.GPIO as GPIO
import os

global ID, curr_pos, target
ID = 0
curr_pos = 0
target = 0

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

def move_mot(nr, angle):
	global curr_pos
	pwm.set_pwm(int(nr),0, int(angle))
	print("move motor"+ str(nr) + " to: "+ str(angle))
	curr_pos = angle
	time.sleep(0.3)
	pwm.set_pwm(int(nr),0,0)

def slomo(nr, angle):
	global curr_pos
	print("target: " + str(target))
	print("angle: " + str(curr_pos))
	diff = target-curr_pos
	print(diff)
	deltad = float(diff)/50
	print(deltad)
	for i in range(0,51):
		pwm.set_pwm(int(nr),0, int(int(curr_pos)+i*float(deltad)))
		print("move motor"+ str(nr) + " to: "+ str(int(curr_pos)+i*float(deltad)))
		time.sleep(0.015)
		pwm.set_pwm(int(nr),0,0)
	curr_pos = angle

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
			target = a
			move_mot(ID, int(a))
	except:
		print(curr_pos)
		if a == u:
			target = curr_pos + 10
			move_mot(ID, target)
		if a == j:
			target = curr_pos - 10
			move_mot(ID, target)

