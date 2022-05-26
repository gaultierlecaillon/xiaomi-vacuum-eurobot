from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO 
import time

kit = ServoKit(channels=8)
tempo = 1
GPIO.setmode(GPIO.BCM)
PUMP_GPIO = 18
GPIO.setup(PUMP_GPIO, GPIO.OUT)

kit.servo[2].angle = 20
time.sleep(0.5)

while True:
    print("down")
    GPIO.output(PUMP_GPIO, False)
    kit.servo[0].angle = 170
    kit.servo[1].angle = 180
    time.sleep(0.5)
    kit.servo[2].angle = 120

    time.sleep(2)

    print("up")
    kit.servo[2].angle = 20
    #GPIO.output(PUMP_GPIO, True)
    time.sleep(0.1)
    kit.servo[1].angle = 30
    kit.servo[0].angle = 15

    time.sleep(1)
