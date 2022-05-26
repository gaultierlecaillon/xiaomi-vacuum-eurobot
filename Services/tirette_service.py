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


class Tirette(Service):

    tiretteGPIO = 4

    def isTirette(self):
        return GPIO.input(self.tiretteGPIO)  # Returns 0 if OFF or 1 if ON

    @Service.action
    def tirette(self, strategy):

        GPIO.setmode(GPIO.BCM)

        # Setup your channel
        GPIO.setup(self.tiretteGPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        while not self.isTirette():
            print("Please put the tirette...")
            time.sleep(1)

        self.publish("Robot ready !")
        while self.isTirette():
            print("Waiting to start the match")
            time.sleep(0.1)

        self.publish(strategy)


async def main():
    tirette_service = Tirette()
    await tirette_service.done()


if __name__ == "__main__":
    asyncio.run(main())
