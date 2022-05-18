from adafruit_servokit import ServoKit
import RPi.GPIO as GPIO
import time

kit = ServoKit(channels=8)
GPIO.setmode(GPIO.BCM)
PUMP_GPIO = 18
GPIO.setup(PUMP_GPIO, GPIO.OUT)

kit.servo[2].angle = 20
time.sleep(1)


print("down")
GPIO.output(PUMP_GPIO, False)
kit.servo[0].angle = 170
kit.servo[1].angle = 145
time.sleep(0.5)
kit.servo[2].angle = 120

time.sleep(1)

print("grab")
kit.servo[2].angle = 20
GPIO.output(PUMP_GPIO, True)
time.sleep(0.2)
kit.servo[0].angle = 80
kit.servo[1].angle = 105

print("lever")
time.sleep(1)
kit.servo[0].angle = 100
time.sleep(0.1)
kit.servo[1].angle = 100

print("deposer")
time.sleep(1)
kit.servo[1].angle = 55
time.sleep(0.1)
kit.servo[0].angle = 30
time.sleep(1)
GPIO.output(PUMP_GPIO, False)

print("fermer")
time.sleep(1)
GPIO.output(PUMP_GPIO, False)
kit.servo[0].angle = 100
time.sleep(0.5)
kit.servo[0].angle = 170
kit.servo[1].angle = 145