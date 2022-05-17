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

from cellaserv.service import Service


class Tirette(Service):

    @Service.coro
    async def initTirette(self):
        # plug on 3.3V and GPIO4 (7)
        channel = 4
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(channel, GPIO.LOW)

        confirmTimeTirette = 5
        confirm = 0
        while True:
            status = bool(GPIO.input(channel))
            if status and confirm < confirmTimeTirette:
                print("ah ?")
                confirm += 1
            elif status and confirm >= confirmTimeTirette:
                print("Tirette is here !")
            else:
                print("No tirette :(")
                confirm = 0
            time.sleep(1)


async def main():
    tirette_service = Tirette()
    await tirette_service.done()


if __name__ == "__main__":
    asyncio.run(main())
