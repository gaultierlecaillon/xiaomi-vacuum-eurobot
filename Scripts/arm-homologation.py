from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time


def moveSlow(servoId, start, to, tempo):
    if start < to:
        for i in range(start, to):
            kit.servo[servoId].angle = i
            time.sleep(tempo)
    else:
        for i in range(to, start):
            kit.servo[servoId].angle = i
            time.sleep(tempo)


# Env
kit = ServoKit(channels=8)
GPIO.setmode(GPIO.BCM)
PUMP_GPIO = 18
GPIO.setup(PUMP_GPIO, GPIO.OUT)

# Init
GPIO.output(PUMP_GPIO, False)
kit.servo[2].angle = 20
time.sleep(0.5)
kit.servo[0].angle = 170
kit.servo[1].angle = 180
time.sleep(0.5)
kit.servo[2].angle = 120
time.sleep(0.5)

# Deploy arm
kit.servo[2].angle = 20
GPIO.output(PUMP_GPIO, True)
time.sleep(0.2)
kit.servo[0].angle = 20
kit.servo[1].angle = 60
time.sleep(0.2)
kit.servo[0].angle = 15
kit.servo[1].angle = 50

# transport

time.sleep(2)
moveSlow(0, 10, 120, 0.01)



