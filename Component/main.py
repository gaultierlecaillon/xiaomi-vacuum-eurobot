from Robot import Robot
#from miio import Vacuum
import threading

#robot = Vacuum("10.10.42.108", "4b4f4b57505552376d5876715a6f4644")
#robot.find()


robot = Robot("192.168.1.27", "7868714171354c436e38704830515450")
robot.startManualMode()
robot.move(90, 0.1, 1000)


