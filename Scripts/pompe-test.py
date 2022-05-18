import RPi.GPIO as GPIO  # import RPi.GPIO module
from time import sleep  # lets us have a delay

GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
PUMP_GPIO = 18
GPIO.setup(PUMP_GPIO, GPIO.OUT)  # set GPIO211 as an output

try:
    while True:
        print("HIGH")
        GPIO.output(PUMP_GPIO, True)
        sleep(2)

        print("LOW")
        GPIO.output(PUMP_GPIO, False)
        sleep(2)

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    GPIO.cleanup()  # resets all GPIO ports used by this program