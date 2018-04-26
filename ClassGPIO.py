import RPi.GPIO as GPIO

def RelayOn():
    GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
    GPIO.setup(18, GPIO.OUT)  # set up pin 18
    GPIO.output(18, 1)  # turn on pin 18
    
def RelayOff():
    GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
    GPIO.setup(18, GPIO.OUT)  # set up pin 18
    GPIO.output(18, 0)  # turn off pin 18

def RelayExchange():
    GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
    GPIO.setup(18, GPIO.OUT)  # set up pin 18
    if GPIO.input(18):
        GPIO.output(18, 0)  # turn off pin 18
    else:
        GPIO.output(18, 1)  # turn on pin 18
