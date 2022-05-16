import time
import serial
import matplotlib.pyplot as plt
import numpy as np

import asyncio
import websockets


class Lidar:
    """ Dictionnary of 360 points angle => [theta, distance_cm, timestamp, ref] """
    points = {}

    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=115200, timeout=1)

        # plt.ion()
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='polar')
        self.ax.set_xticks(np.arange(0, 2.0 * np.pi, np.pi / 6.0))
        self.ax.set_ylim(0, 100)
        self.ax.set_yticks(np.arange(0, 2, 25.0))

    def cleanPackage(self, line):
        package = str(line.rstrip()).replace("b'", '').replace("'", '').strip().split(' ')

        for i in range(len(package)):
            package[i] = package[i].zfill(2)
            package[i] = int(package[i], base=16)
        return package


    def checksum(self, data):
        """Compute and return the checksum as an int.
        data -- list of 20 bytes (as ints), in the order they arrived in.
        """
        # group the data by word, little-endian
        data_list = []
        for t in range(10):
            data_list.append(data[2 * t] + (data[2 * t + 1] << 8))

        # compute the checksum on 32 bits
        chk32 = 0
        for d in data_list:
            chk32 = (chk32 << 1) + d

        # return a value wrapped around on 15bits, and truncated to still fit into 15 bits
        checksum = (chk32 & 0x7FFF) + (chk32 >> 15)  # wrap around to fit into 15 bits
        checksum = checksum & 0x7FFF  # truncate to 15 bits
        return int(checksum)

    def dataFromBytes(self, angle, data):
        """Interpres the data bytes into a more readable form"""
        # Individual bytes
        x0 = data[0]
        x1 = data[1]
        x2 = data[2]
        x3 = data[3]

        dist_mm = x0 | ((x1 & 0x3f) << 8)
        quality = x2 | (x3 << 8)

        if quality > 0:
            angle = 90 - angle  # correct angle so angle 0 is in front

            theta = np.deg2rad(angle)
            self.points[angle] = [
                angle,
                theta,
                dist_mm / 10,
                time.time(),
                None  # self.ax.scatter(theta, dist_mm / 10)
            ]

    def decodePackage(self, package):
        # Speed byte
        b_speed = [package[2], package[3]]

        # Data bytes
        b_data0 = [package[4], package[5], package[6], package[7]]
        b_data1 = [package[8], package[9], package[10], package[11]]
        b_data2 = [package[12], package[13], package[14], package[15]]
        b_data3 = [package[16], package[17], package[18], package[19]]

        # The whole data packet
        all_data = [0xFA, package[1]] + b_speed + b_data0 + b_data1 + b_data2 + b_data3

        # Checksum
        b_checksum = [package[20], package[21]]
        incoming_checksum = int(b_checksum[0]) + (int(b_checksum[1]) << 8)

        # Verify that the received checksum is equal to the one computed from the data
        if self.checksum(all_data) == incoming_checksum:
            # speedRPM = self.compute_speed(b_speed)
            self.dataFromBytes((package[1] - 0xA0) * 4 + 0, b_data0)
            self.dataFromBytes((package[1] - 0xA0) * 4 + 1, b_data1)
            self.dataFromBytes((package[1] - 0xA0) * 4 + 2, b_data2)
            self.dataFromBytes((package[1] - 0xA0) * 4 + 3, b_data3)
            print(package)

    def startScan(self, maxTimeScan):
        start_time = time.time()
        execTime = 0
        count = 0

        while execTime < maxTimeScan:
            arduinoData = self.ser.readline()
            package = self.cleanPackage(arduinoData)

            if package != [0]:
                self.decodePackage(package)

            execTime = time.time() - start_time
            count += 1

        self.ser.close()

        print("count:", count)
        print("len:", len(self.points))

    def display(self):
        #self.points(angle, theta, dist_mm, time, ref)
        for index in self.points:
            point = self.points[index]
            self.ax.scatter(point[1], point[2])
        plt.show()

    def isObstacle(self):
        # self.points(angle, theta, dist_mm, time, ref)

        pointInFront = {}
        nbConfirmation = 5
        targetDistanceCm = 30
        maxAge = 5
        count = 0

        for angle in range(30, 150):
            if angle in self.points and self.points[angle][2] < targetDistanceCm and time.time() - self.points[angle][3] < maxAge:
                count += 1
                pointInFront[count] = self.points[angle]

        print(pointInFront)
        return len(pointInFront) >= nbConfirmation

lidar = Lidar('COM3')
lidar.startScan(4)
lidar.display()
print("is an Obstacle ?", lidar.isObstacle())
