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
import logging
import os
import shutil


class main:

    def __init__(self):
        self.ei = ErrorIndicator(True)
        self.ih = ImageHandler(True, self.ei)  # TODO Be False
        self.processor = ImageProcessor(self.ih, self.ei)
        self.arduino = Arduino(self.ei)

        if os.path.exists("out/"):
            shutil.rmtree("out")
        os.makedirs("out")
        if os.path.exists("log.txt"):
            os.remove("log.txt")

        logging.basicConfig(filename='log.txt', level=logging.DEBUG,
                            format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    def standby(self):
        if self.check_arduino(False):
            logging.info("Waiting for GPS fix..")
            self.ei.message([0, 0, 0, 1])
            time.sleep(0.5)
            self.ei.message([0, 0, 0, 0])
            time.sleep(0.5)
            return True

    def check_arduino(self, initial):
        success = True
        if initial:
            if not main.arduino.init():
                self.ei.message([1, 0, 0, 0])
                success = False
        if main.arduino.get_dof_error():
            self.ei.message([1, 1, 1, 0])
            success = False
        if main.arduino.get_gps_error():
            self.ei.message([0, 1, 1, 0])
            success = False
        if success:
            self.ei.message([0, 0, 0, 0])
        return success

    def check_pi(self):
        if self.ih.camera_error():
            self.ei.message([1, 1, 0, 0])
            return False
        self.ei.message([0, 0, 0, 0])
        return True

    def run(self, count):
        logging.info("*********************" + str(count) + "*********************")
        #current_altitude = self.arduino.get_altitude() * 3.28084  # ft
        current_altitude = 500  # TODO temp holder
        logging.info("Current Altitude: " + str(current_altitude))

        #current_distance = self.arduino.get_distance() * 3.28084  # ft
        current_distance = 400  # TODO temp holder
        logging.info("Current Distance: " + str(current_distance))


        #total_tarp_are = Tc.get_total_tarp_area(current_altitude, current_distance)  # pixels^3
        #single_tarp_area = Tc.get_single_tarp_area(current_altitude, current_distance)  # pixels^3
        single_tarp_area = 1000  # TODO temp holder
        total_tarp_are = 4000  # TODO temp holder

        logging.info("Creating Background Mask")
        self.processor.create_background_mask()
        logging.info("Filtering by size")
        self.processor.filter_by_size((total_tarp_are * 0.6, total_tarp_are))  # 0.007 TODO allow method to control size and adjust like blur_thresh
        logging.info("Getting Tarp Mask")
        self.processor.get_tarps()
        logging.info("Saving Tarps")
        self.processor.save_tarps(count, single_tarp_area)

    def init(self):
        return self.check_arduino(True) and self.check_pi()

is_deployed, is_in_rocket, waiting_to_start = False, False, True

main = main()

while waiting_to_start:
    main.ei.message([1, 1, 1, 1])
    time.sleep(5)

main.ei.message([0, 0, 0, 0])

logging.info("Initializing main")
if not main.init():
    while not main.check_arduino(False) or not main.check_pi():
        time.sleep(5)
        logging.info("Waiting for Arduino or Pi")
logging.info("Main Initialized")

while not is_in_rocket:
    logging.info("Waiting to be inside rocket")
    time.sleep(1)

    while not main.arduino.gps_has_fix():
        main.standby()
        if is_in_rocket:
            break
        break  # TODO Uncomment

    if main.check_arduino(False) and main.check_pi():
        main.ei.message([0, 0, 0, 1])

    is_in_rocket = True  # TODO Uncomment
logging.info("Inside Rocket")

while is_in_rocket:
    logging.info("Waiting for Erection(Ejection)")
    if not main.arduino.gps_has_fix():
        logging.info("Inside rocket, no GPS fix..")
    time.sleep(1)
    is_in_rocket = False  # TODO Uncomment
    is_deployed = True  # TODO Uncomment
logging.info("Ejected!")

counter = 0

t = time.time()
while is_deployed:
    if time.time() - t > 5:  # TODO Remove
        break
    '''if main.arduino.get_altitude() < 10:
        false_positive = False
        for i in range(0, 10):
            if main.arduino.get_altitude() > 10:  # So a goofy missread doesn't screw us
                false_positive = True
        if not false_positive:
            logging.info("Below 10m, Quiting!")
            break'''
    main.run(counter)
    counter += 1

main.processor.scores = sorted(main.processor.scores)
logging.info("Scores (First is best): " + str(main.processor.scores))

