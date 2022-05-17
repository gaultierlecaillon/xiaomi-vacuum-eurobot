import RPi.GPIO as GPIO
import time

# plug on 3.3V and GPIO4 (7)
channel = 4
GPIO.setmode(GPIO.BCM)
# Setup your channel
GPIO.setup(channel, GPIO.OUT)
GPIO.output(channel, GPIO.LOW)


def tiretteStatus():
    return GPIO.input(channel)  # Returns 0 if OFF or 1 if ON

while True:
    print(tiretteStatus())
    time.sleep(0.5)