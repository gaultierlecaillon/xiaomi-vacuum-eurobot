#!/usr/bin/env python3
import time
from random import randrange
import asyncio
import os
import sys
import inspect
from adafruit_servokit import ServoKit

''' Import cellaserv submodul '''
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
grandParentdir = os.path.dirname(parentdir)
sys.path.insert(0, grandParentdir + '/python-cellaserv3/')
sys.path.insert(0, parentdir + '/Component/')
from cellaserv.service import Service
from Robot import Robot
import RPi.GPIO as GPIO

kit = ServoKit(channels=8)
GPIO.setmode(GPIO.BCM)
PUMP_GPIO = 18
GPIO.setup(PUMP_GPIO, GPIO.OUT)


def initArm():
    GPIO.output(PUMP_GPIO, False)
    kit.servo[2].angle = 20
    time.sleep(0.5)
    kit.servo[0].angle = 170
    kit.servo[1].angle = 170
    time.sleep(0.5)
    kit.servo[2].angle = 120

def moveSlow(servoId, start, to, tempo):
    if start < to:
        for i in range(start, to):
            kit.servo[servoId].angle = i
            time.sleep(tempo)
    else:
        for i in range(start, to, -1):
            kit.servo[servoId].angle = i
            time.sleep(tempo)


def getDistance():
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)

    # set GPIO Pins
    GPIO_TRIGGER = 23
    GPIO_ECHO = 24

    # set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.01)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    GPIO.cleanup()

    return int(distance)


class Xiaomi(Service):
    robot = None

    @Service.action
    async def startManualMode(self):
        self.robot = Robot("192.168.0.103", "30564f3765306d65306772654254546c")
        self.robot.startManualMode()
        self.publish("initSensor")
        initArm()

    @Service.action
    def placement(self, color):
        if color == "V":
            self.robot.move(0, 0.1, 5000)
        elif color == "J":
            self.robot.move(0, -0.1, 5000)
        time.sleep(5)


    def grabDistributeur(self):
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


    @Service.event("startHomologationJ")
    def startHomologationJ(self):
        self.robot.move(0, 0.1, 5000)
        time.sleep(5)

        self.grabDistributeur()

        self.robot.move(-5, -0.1, 2000)
        time.sleep(2)

        # Depose
        moveSlow(0, 120, 10, 0.01)
        GPIO.output(PUMP_GPIO, False)
        time.sleep(4)
        initArm()

        self.robot.move(50, 0, 2000)
        time.sleep(2)

        self.robot.move(0, 0.2, 2000)
        time.sleep(2)



    @Service.event("stop")
    def stop(self):
        self.publish("Stoping")
        self.robot.move(0, 0, 3000)

    @Service.event("obstacle")
    async def obstacle(self):
        self.robot.move(0, 0, 1000)
        time.sleep(0.5)
        self.publish("initSensor")

    @Service.action
    async def move(self, theta, dist, time):
        self.robot.move(theta, dist, time)


async def main():
    xiaomi_service = Xiaomi()
    await xiaomi_service.done()


if __name__ == "__main__":
    asyncio.run(main())
