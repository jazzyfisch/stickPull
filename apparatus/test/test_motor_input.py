import Adafruit_PCA9685
import time
import RPi.GPIO as GPIO
import os

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)

def move_mot(nr, angle):
	pwm.set_pwm(int(nr),0, int(angle))
	time.sleep(0.5)
	pwm.set_pwm(int(nr),0,0)

while True:
	a = input()
