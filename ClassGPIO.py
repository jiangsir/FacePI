import RPi.GPIO as GPIO

pin = 18
GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom
GPIO.setup(pin, GPIO.OUT)  # set up pin 18

def RelayOn():
    GPIO.output(pin, 1)  # turn on pin 18
    
def RelayOff():
    GPIO.output(pin, 0)  # turn off pin 18

def RelayExchange():
    if GPIO.input(pin):
        GPIO.output(pin, 0)  # turn off pin 18
    else:
        GPIO.output(pin, 1)  # turn on pin 18
