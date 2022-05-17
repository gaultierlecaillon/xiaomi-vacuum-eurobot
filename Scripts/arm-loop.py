from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=8)
tempo = 1

kit.servo[2].angle = 20
time.sleep(0.5)

while True:
    print("down")
    kit.servo[0].angle = 170
    kit.servo[1].angle = 160
    time.sleep(0.5)
    kit.servo[2].angle = 120

    time.sleep(2)

    print("up")
    kit.servo[2].angle = 20
    time.sleep(0.1)
    kit.servo[1].angle = 15
    kit.servo[0].angle = 15
    time.sleep(1)
