#this code is for testing the IR Sensor

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
IRPin = 17
GPIO.setup(IRPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
try:
    while True:
        IRState = GPIO.input(IRPin)
        print(IRState)
        time.sleep(.1)
except:
    GPIO.cleanup()
    print('GPIO Good to go')