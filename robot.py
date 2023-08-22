from Raspi_MotorHAT import Raspi_MotorHAT
from gpiozero import LineSensor

import atexit


class Robot(object):


    # code to set up motor hat, get the left and right motors, and register a stop system
    def __init__(self, motorhat_addr=0x6f):

        # setup the motorhat with the passed in address
        self._mh = Raspi_MotorHAT(addr=motorhat_addr)

        # get local variable for each motor
        self.left_motor = self._mh.getMotor(1)
        self.right_motor = self._mh.getMotor(2)

        # ensure the motors get stopped when the code exits
        atexit.register(self.stop_all)

        # setup the line sensors
        self.left_line_sensor = LineSensor(23, pull_up=True)
        self.right_line_sensor = LineSensor(16, pull_up=True)

    def stop_all(self):
        self.stop_motors() # stop the motors when code exits

        # clear any sensor handlers when code exits to stop the line sensors from activating
        # the motors after they have been stopped
        self.left_line_sensor.when_line = None
        self.left_line_sensor.when_no_line = None
        self.right_line_sensor.when_line = None
        self.right_line_sensor.when_no_line = None


    # transfer to specific motor speed (0 to 255) from input (-100 to 100)
    # and determines movement direction based on positive or negative input
    # takes in speed as an input parameter to self
    # returns mode (forward, backward, or release), speed (0 to 255)
    def convert_speed(self, speed): 

        # choose the running mode
        mode = Raspi_MotorHAT.RELEASE
        if speed > 0:
            mode = Raspi_MotorHAT.FORWARD
        elif speed < 0:
            mode = Raspi_MotorHAT.BACKWARD

        # scale the speed 
        output_speed = (abs(speed) * 255) / 100
        return mode, int(output_speed)


    # set_left and set_right methods take speed (-100 to 100) to move respective motors
    # set_left and set_right will get a mode and an output speed from passed-in speed
    # they will call setSpeed and run methods from motorHat code
    def set_left(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.left_motor.setSpeed(output_speed)
        self.left_motor.run(mode)

    def set_right(self, speed):
        mode, output_speed = self.convert_speed(speed)
        self.right_motor.setSpeed(output_speed)
        self.right_motor.run(mode)


    def stop_motors(self):
        self.left_motor.run(Raspi_MotorHAT.RELEASE)
        self.right_motor.run(Raspi_MotorHAT.RELEASE)

