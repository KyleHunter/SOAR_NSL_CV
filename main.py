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

class main:

    def __init__(self):
        self.ei = ErrorIndicator(True)
        self.ih = ImageHandler(True, self.ei)
        self.processor = ImageProcessor(self.ih, self.ei)
        self.arduino = Arduino(self.ei)

    def standby(self):
        if self.check_arduino(False):
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
        return success

    def check_pi(self):
        if self.ih.camera_error():
            self.ei.message([1, 1, 0, 0])
            return False
        return True

    def run(self):
        self.ih.take_image()

        current_altitude = 500  # ft
        single_tarp_area = Tc.get_total_tarp_area(current_altitude)  # pixels^3
        single_tarp_area = 3000  # place holder

        self.processor.create_background_mask()  # 0.1
        self.processor.filter_by_size((3000, 4000))  # 0.007
        self.processor.get_tarps()  # 0.015
        self.processor.save_tarps()  # 0.19

    def init(self):
        return self.check_arduino(True) and self.check_pi()

is_deployed, is_in_rocket = False, False

main = main()

if not main.init():
    while not main.check_arduino(False) or not main.check_pi():
        time.sleep(5)

while not is_in_rocket:
    main.check_arduino(False)
    main.check_pi()
    time.sleep(5)

