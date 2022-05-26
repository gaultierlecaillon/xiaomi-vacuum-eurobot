import asyncio
import os
import sys
import inspect
import time

''' Import cellaserv submodul '''
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir + '/python-cellaserv3/')

from cellaserv.proxy import CellaservProxy


async def main():
    cs = CellaservProxy()

    await asyncio.wait([
        cs.date.time(),
        cs.xiaomi.startManualMode()
    ])

    await cs.xiaomi.move(0, 0.1, 5000)
    time.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
