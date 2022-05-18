from adafruit_servokit import ServoKit
import time
import sys
import RPi.GPIO as GPIO

kit = ServoKit(channels=8)
PUMP_GPIO = 18
GPIO.setup(PUMP_GPIO, GPIO.OUT)
GPIO.output(PUMP_GPIO, True)
kit.servo[0].angle = 170
kit.servo[1].angle = 145
kit.servo[2].angle = 20

while True:
    print('What the angle for Servo 0 ?')
    angle = int(input())
    if angle > 0:
        kit.servo[0].angle = angle

    print('What the angle for Servo 1 ?')
    angle = int(input())
    if angle > 0:
        kit.servo[1].angle = angle



'''

while True:
    kit.servo[0].angle = 170
    kit.servo[1].angle = 140
    time.sleep(2)

    kit.servo[0].angle = 15
    kit.servo[1].angle = 20

    time.sleep(2)

'''