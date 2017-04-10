'''
*   main.py is primary file which calls needed methods
*
*   will be only file called on runtime
'''

from ImageHandler import ImageHandler
from ImageProcessor import ImageProcessor
import TarpCalculation as Tc
from Arduino import Arduino
from ErrorIndicator import ErrorIndicator
import time
import os
import shutil
import RPi.GPIO as GPIO
import Log
import logging

main_logger, orientation_logger = logging.getLogger("SOAR.main_logger"), logging.getLogger("SOAR.orientation_logger")


class main:
    def __init__(self):
        """
        Sets up program variables, resets files, does not tell arduino to start
        """
        GPIO.setmode(GPIO.BCM)
        self.ei = ErrorIndicator(False)
        self.ih = ImageHandler(False, self.ei)
        self.processor = ImageProcessor(self.ih, self.ei)
        self.arduino = Arduino(self.ei)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(25, GPIO.IN)
        GPIO.setwarnings(False)

        if os.path.exists("out/"):
            shutil.rmtree("out")
        os.makedirs("out")
        if os.path.exists("log.txt"):
            os.remove("log.txt")

        Log.setup_log()

    def check_for_gps_fix(self):
        """
        Checks for GPS fix, flashes error if not
        :return: True if GPS has a fix
        """
        if not main.arduino.gps_has_fix():
            main_logger.info("Waiting for GPS fix..")
            self.ei.message([0, 0, 0, 1])
            time.sleep(0.5)
            self.ei.message([0, 0, 0, 0])
            time.sleep(0.5)
            return False
        return True

    def check_arduino(self, initial):
        """
        Checks to make sure arduino sensors are working, no check for GPS fix
        :param initial: First time being called, checks if comms with arduino work
        :return: If no errors are present
        """
        success = True
        if initial:
            if not main.arduino.init():
                self.ei.message([1, 0, 0, 0])
                return False
        if main.arduino.get_dof_error():
            self.ei.message([1, 1, 1, 0])
            success = False
        if main.arduino.get_gps_error():
            self.ei.message([0, 1, 1, 0])
            success = False
        if success:
            self.ei.reset()
        return success

    def check_pi(self):  # TODO handle exception issue
        """
        Checks if the camera on Pi is working
        :return: False if camera is too dark
        """
        if self.ih.camera_error():
            self.ei.message([1, 1, 0, 0])
            return False
        self.ei.reset()
        return True

    def run(self, count):
        """
        Method run while lander is in decent
        :param count: Number of loops called (Used for logger)
        """
        main_logger.info("*********************" + str(count) + "*********************")
        current_altitude = self.arduino.get_altitude() * 3.28084  # ft
        main_logger.info("Current Altitude: " + str(current_altitude))

        current_distance = self.arduino.get_distance() * 3.28084  # ft
        main_logger.info("Current Distance: " + str(current_distance))

        total_tarp_area = Tc.get_total_tarp_area(current_altitude, current_distance)  # pixels^3

        main_logger.info("Creating Background Mask")
        self.processor.create_background_mask()
        main_logger.info("Filtering by size")
        self.processor.filter_by_size(total_tarp_area)
        main_logger.info("Getting Tarp Mask")
        self.processor.get_tarps()
        main_logger.info("Saving Tarps")
        self.processor.save_tarps(count)

    @staticmethod
    def told_to_start():  # Wire GPIO 24 to button to ground
        """
        Determines if switch is on, telling us to start the arduino and enter standby
        :return: True if switch is closed
        """
        if not GPIO.input(24):
            return True
        return False

    @staticmethod
    def told_to_end():  # Wire GPIO 24 to button to ground
        """
        Determines if switch is off, telling us to ensure loops are ended and to save log
        :return: True if switch is open
        """
        if GPIO.input(24):
            return True
        return False

    def starting_notification(self):
        self.ei.message([1, 1, 1, 1])
        self.ei.turn_buzzer_on()
        time.sleep(5)
        self.ei.turn_buzzer_off()
        self.ei.reset()

    def second_notification(self):
        for i in range(0, 10):
            self.ei.message([1, 1, 1, 1])
            self.ei.turn_buzzer_on()
            time.sleep(0.5)
            self.ei.turn_buzzer_off()
            self.ei.reset()

    def third_notification(self):
        self.ei.message([1, 1, 1, 1])
        self.ei.turn_buzzer_on()
        time.sleep(5)
        self.ei.turn_buzzer_off()
        self.ei.reset()

    @staticmethod
    def is_in_rocket():  # Connect photoresistor to GPIO 25
        """
        Checks if lander is in rocket by using a photoresistor
        :return: True if in rocket
        """
        if GPIO.input(25):
            return True
        else:
            return False

    def is_at_low_altitude(self):
        """
        Checks if lander is under 10m
        :return: True if under 10m in air
        """
        if self.arduino.get_altitude() < 10:
            false_positive = False
            for i in range(0, 10):
                if main.arduino.get_altitude() > 10:  # So a goofy misread doesn't screw us
                    false_positive = True
            if not false_positive:
                return True

    def init(self):
        """
        Initializes arduino, turning all sensors on and placing in standby
        :return: True if arduino and pi have no errors (No check for GPS)
        """
        return self.check_arduino(True) and self.check_pi()

#  TODO Wrap Exceptions
main = main()

#  Waits for switch to tell Pi to have everything start
while not main.told_to_start():
    time.sleep(3)
main_logger.info("Initializing main")
main.starting_notification()


#  Starts Arduino and does initial check of all systems (Not looking for GPS fix)
if not main.init():
    while not main.check_arduino(False) or not main.check_pi():
        time.sleep(3)
        main_logger.info("Arduino or Pi have errors..")
        if main.told_to_end():  # Just in case..
            break
main_logger.info("Main Initialized")


#  Waits outside rocket, checking for errors and GPS fix
in_count = 0
while in_count < 20:  # 20*3 = 60s of consistent darkness
    main_logger.info("Waiting to be inside rocket")
    while not main.arduino.gps_has_fix():
        main.check_for_gps_fix()
        main_logger.info("Outside rocket, no GPS fix..")

    if main.check_arduino(False) and main.check_pi():
        main.ei.message([0, 0, 0, 1])
    else:
        main_logger.info("Arduino or Pi have errors..")
    time.sleep(3)
    if main.told_to_end():  # Just in case..
        break
    if main.is_in_rocket():
        in_count += 1
    else:
        in_count = 0
main_logger.info("Inside Rocket")
main.second_notification()


#  Lander is inside rocket, still checks for errors with arduino(Can hear buzzer)
while main.is_in_rocket():
    main_logger.info("Waiting for Ejection")
    if not main.arduino.gps_has_fix():
        main_logger.info("Inside rocket, no GPS fix..")
    if main.check_arduino(False):
        main.ei.message([0, 0, 0, 0])  # Can't see the error anyway..
        main_logger.info("Inside Rocket, error with Arduino")
    time.sleep(3)
    if main.told_to_end():  # Just in case..
        break
main_logger.info("Ejected!")
main.third_notification()

#  Lander is outside rocket, no error checks as it's irrelevant, takes images
time.sleep(15)  # Ensure parachute and everything is cleared before initializing camera servos TODO Determine how long
counter = 0
start_time = time.time()
while True:
    run_time = time.time() - start_time
    loop_time = time.time()
    main_logger.info("GPS: " + str(main.arduino.get_lattitude) + ", " + str(main.arduino.get_longitude))
    orientation_logger.info(Log.o_format(run_time, main.arduino.get_orientations()))
    if main.is_at_low_altitude():
        main_logger.info("Below 10m, Quiting!")
        break
    main.run(counter)
    counter += 1
    if main.told_to_end():  # Just in case..
        break
    while time.time() - loop_time < 1:  # Sleep a min of 1 sec
        time.sleep(0.1)


main.arduino.shutdown()
main.processor.scores = sorted(main.processor.scores)
main_logger.info("Scores (First is best): " + str(main.processor.scores))

