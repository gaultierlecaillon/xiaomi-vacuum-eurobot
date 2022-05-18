#!/usr/bin/env python3
import time
from random import randrange
import asyncio
import os
import sys
import inspect

''' Import cellaserv submodul '''
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
grandParentdir = os.path.dirname(parentdir)
sys.path.insert(0, grandParentdir + '/python-cellaserv3/')
sys.path.insert(0, parentdir + '/Component/')
from cellaserv.service import Service
from Robot import Robot


class Xiaomi(Service):

    robot = None

    @Service.action
    async def startManualMode(self):
        self.robot = Robot("192.168.0.103", "30564f3765306d65306772654254546c")
        self.robot.startManualMode()
        self.publish("manualModeStarted")

    @Service.event("startMatch")
    def startMatch(self):
        self.robot.move(0, 0.1, 2000)
        time.sleep(2)

    @Service.event("startHomologation")
    def startHomologation(self):
        self.robot.move(90, 0, 2000)
        time.sleep(2)

    @Service.event("stop")
    def stop(self):
        self.publish("Stoping")
        self.robot.move(0, 0, 3000)

    @Service.action
    async def move(self, theta, dist, time):
        self.publish("Moving for real")
        self.robot.move(theta, dist, time)


async def main():
    xiaomi_service = Xiaomi()
    await xiaomi_service.done()


if __name__ == "__main__":
    asyncio.run(main())
