#!/usr/bin/env python3
import time
from random import randrange
import asyncio
import os
import sys
import inspect
import RPi.GPIO as GPIO

''' Import cellaserv submodul '''
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
grandParentdir = os.path.dirname(parentdir)
sys.path.insert(0, grandParentdir + '/python-cellaserv3/')
from cellaserv.service import Service


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


class Ultrasonic(Service):

    @Service.event("initSensor")
    async def initSensor(self):
        trigger = 20  # in cm
        confirmation = 0

        while True:
            dist = getDistance()
            print("Dist:", dist)
            if dist <= trigger:
                confirmation += 1
            else:
                confirmation = 0

            if confirmation >= 3:
                self.publish("obstacle")
                break

            time.sleep(0.1)


async def main():
    ultrasonic_service = Ultrasonic()
    await ultrasonic_service.done()


if __name__ == "__main__":
    asyncio.run(main())
