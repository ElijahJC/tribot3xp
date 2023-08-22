
from Raspi_MotorHAT import Raspi_MotorHAT # library for interacting with motors
import time # time library to work with time durations
import atexit # atexit allows us to run code when file exits

# connecting the motor hat and the two motors
mh = Raspi_MotorHAT(addr=0x6f) # moter hat object with 12C address passed in
lm = mh.getMotor(1) # left motor mh, motor numbers shown on board (motor 1 is left motor)
rm = mh.getMotor(2) # right motor from mh (motor 2 is right motor)

# function to RELEASE each motor (an instruction to make the motors stop)
def turn_off_motors(): 
    lm.run(Raspi_MotorHAT.RELEASE)
    rm.run(Raspi_MotorHAT.RELEASE)

# force the motors off when the file finishes, or when Python exits, even if there are errors
atexit.register(turn_off_motors)

# code to set speed for motors (just above half speed)
lm.setSpeed(150)
rm.setSpeed(150)

# makes each motor drive forward
lm.run(Raspi_MotorHAT.FORWARD)
rm.run(Raspi_MotorHAT.FORWARD)

# ask the code to wait for one second
time.sleep(1)

# motors will then stop from the atexit() command, since the file is finished