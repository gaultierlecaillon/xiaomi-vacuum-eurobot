from miio import Vacuum
#from adafruit_servokit import ServoKit
import time

class Robot:
    Vac = None  # Miio instance
    ip = None
    token = None

    debug = True
    #kit = ServoKit(channels=8)

    def __init__(self, _ip, _token):
        self.ip = _ip
        self.token = _token
        self.initRobot()
        print("Robot Initialization")

    def find(self):
        if self.debug:
            print("Hello je suis là !")
        self.Vac.find()
        time.sleep(1)

    def initRobot(self):
        self.Vac = Vacuum(self.ip, self.token)
        self.Vac.set_fan_speed(0)

        '''
        self.kit.servo[0].angle = 140
        self.kit.servo[1].angle = 160
        time.sleep(1)
        self.kit.servo[0].angle = 0
        self.kit.servo[1].angle = 30
        time.sleep(1)
        self.kit.servo[0].angle = 140
        self.kit.servo[1].angle = 160
        '''

    def startManualMode(self):
        if self.debug:
            print("Starting Manual Mode...")

        self.Vac.manual_start()
        number_of_tries = 3
        while number_of_tries > 0:
            if self.Vac.status().state_code == 7:
                print('Starting vacuum...')
                time.sleep(7)
                break
            else:
                print('Error vacuum code: ', self.Vac.status().state_code)
                print('Decode Error: ', self.decodeError(self.Vac.status().state_code))

            print("Try left ", number_of_tries)
            number_of_tries -= 1
            time.sleep(1)
        print("Robot Ready")

    def move(self, rotation, velocity, duration):
        if self.debug:
            print("Moving Robot...")

        self.Vac.manual_control(rotation, velocity, duration)
        time.sleep(duration / 1000)

        print("Done Moving Robot...")

    def stop(self):
        if self.debug:
            print("Stoping Robot...")

        self.Vac.manual_stop()

    def decodeError(self, code):
        error_codes = {
            0: "No error",
            1: "Laser distance sensor error",
            2: "Collision sensor error",
            3: "Wheels on top of void, move robot",
            4: "Clean hovering sensors, move robot",
            5: "Clean main brush",
            6: "Clean side brush",
            7: "Main wheel stuck?",
            8: "Device stuck, clean area",
            9: "Dust collector missing",
            10: "Clean filter",
            11: "Stuck in magnetic barrier",
            12: "Low battery",
            13: "Charging fault",
            14: "Battery fault",
            15: "Wall sensors dirty, wipe them",
            16: "Place me on flat surface",
            17: "Side brushes problem, reboot me",
            18: "Suction fan problem",
            19: "Unpowered charging station",
        }
        return error_codes[int(code)]
