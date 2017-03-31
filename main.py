'''
*   main.py is primary file which calls needed methods
*
*   will be only file called on runtime
'''


from ImageHandler import ImageHandler
from ImageProcessor import ImageProcessor
import TarpCalculation as tc

ih = ImageHandler(True)
ip = ImageProcessor(ih)

ih.take_image()
#ih.resize_image(902, 327)

current_altitude = 500  # ft
single_tarp_area = tc.get_tarp_area(current_altitude)  # pixels^3
single_tarp_area = 3000  # place holder

ip.create_tarp_mask()
ip.filter_by_size((500, 5000))
ip.get_tarps()
ip.debug()








