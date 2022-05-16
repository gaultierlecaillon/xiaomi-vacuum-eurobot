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

from cellaserv.service import Service


class Tirette(Service):

    @Service.event("lol")
    async def lol(self):
        self.publish('lol')


async def main():
    tirette_service = Tirette()
    await tirette_service.done()


if __name__ == "__main__":
    asyncio.run(main())
