import RPi.GPIO as GPIO
import time

def readLight():
    count = 0

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)
    GPIO.output(23, 0)
    time.sleep(1)
    GPIO.setup(23, GPIO.IN)

    while (GPIO.input(23) == 0)
        count += 1

    return round((100 - (count * 0.0008)), 2)

while True:
    print(readLight())