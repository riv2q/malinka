import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT)
GPIO.output(11, 1)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, 1)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, 1)
import time
try:
    while(True):
        GPIO.output(11, 1)
        GPIO.output(13, 0)
        GPIO.output(15, 1)
        time.sleep(1)
        GPIO.output(11, 0)
        GPIO.output(13, 1)
        GPIO.output(15, 1)
        time.sleep(1)
        GPIO.output(11, 1)
        GPIO.output(13, 1)
        GPIO.output(15, 0)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
