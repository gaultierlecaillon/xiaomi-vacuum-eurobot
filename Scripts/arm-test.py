from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=8)

servo = 2

kit.servo[0].angle = 170
kit.servo[1].angle = 160
kit.servo[2].angle = 120

while True:
    print('What the angle for Servo ', servo, ' ?')
    angle = int(input())
    kit.servo[servo].angle = angle



'''

while True:
    kit.servo[0].angle = 170
    kit.servo[1].angle = 140
    time.sleep(2)

    kit.servo[0].angle = 15
    kit.servo[1].angle = 20

    time.sleep(2)

'''