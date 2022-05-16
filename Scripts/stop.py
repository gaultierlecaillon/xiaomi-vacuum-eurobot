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
from Robot import Robot

robot = Robot("192.168.1.31", "4c4a42696a4157707a77304867473241")
robot.move(90, 0.1, 1000)
