'''
*   TarpCalculation.py handles math with the size of the tarps
*
*   All static methods
'''


def get_tarp_width(altitude):
    return 40 * 5580.2 * altitude ** -1.117


def get_tarp_area(altitude):
    return get_tarp_width(altitude) * 4


def get_total_tarp_area(altitude):
    return get_tarp_area(altitude) * 3
