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
from cellaserv.service import Service


class Date(Service):
    @Service.action
    async def time(self):
        return int(time.time())

    @Service.action
    async def print_async(self):
        print(time.time())

    @Service.event("startMatch")
    async def startChrono(self):
        current_time = time.time()
        time_spend = time.time() - current_time
        while time_spend < 100:
            print("Match started", int(time_spend), "s ago")
            time_spend = time.time() - current_time
            time.sleep(1)
        self.publish("stop")

    @Service.coro
    async def timer(self):
        while not self._disconnect:
            self.log(time=time.time())
            await asyncio.sleep(3)


async def main():
    date_service = Date()
    await date_service.done()


if __name__ == "__main__":
    asyncio.run(main())