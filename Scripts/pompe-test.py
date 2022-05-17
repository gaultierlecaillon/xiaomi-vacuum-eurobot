import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep  # lets us have a delay

GPIO.setmode(GPIO.BOARD)  # choose BCM or BOARD
GPIO.setup(11, GPIO.OUT)  # set GPIO211 as an output

try:
    while True:
        print("HIGH")
        GPIO.output(11, GPIO.HIGH)
        sleep(2)

        print("LOW")
        GPIO.output(11, GPIO.LOW)
        sleep(2)

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()  # resets all GPIO ports used by this program