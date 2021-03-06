import RPi.GPIO as GPIO
import configparser

config = configparser.ConfigParser()
config.read('/home/pi/Documents/stickPull/config.conf')
print (config['PIN_BUTTON'])
# PINS
button_L2 = int(config['PIN_BUTTON']['L2']) # 13 # config.buttons["button_R1"] L2
button_L1 = int(config['PIN_BUTTON']['L1']) # 6 # L1
button_R1 = int(config['PIN_BUTTON']['R1']) # 11 # R1
button_R2 = int(config['PIN_BUTTON']['R2']) # 5 #R2

GPIO.setmode(GPIO.BCM)
GPIO.setup(button_R1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_R2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_L1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(button_L2, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(button_R1, GPIO.FALLING, bouncetime=300)
GPIO.add_event_detect(button_R2, GPIO.FALLING, bouncetime=300)
GPIO.add_event_detect(button_L1, GPIO.FALLING, bouncetime=300)
GPIO.add_event_detect(button_L2, GPIO.FALLING, bouncetime=300)
    
    
while True:
    '''    if not(GPIO.input(button_R1)):
        print("button R1 is pressed")
    if not(GPIO.input(button_L1)):
        print("button L1 is pressed")
    if not(GPIO.input(button_R2)):
        print("button R1 is pressed")
    if not(GPIO.input(button_L2)):
        print("button L1 is pressed")
        '''
    if GPIO.event_detected(button_R1):
        print("button R1")
    if GPIO.event_detected(button_L1):
        print("button L1")
    if GPIO.event_detected(button_R2):
        print("button R2")
    if GPIO.event_detected(button_L2):
        print("button L2")
