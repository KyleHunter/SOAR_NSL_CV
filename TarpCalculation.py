'''
*   TarpCalculation.py handles math with the size of the tarps
*
*   All static methods
'''


def get_tarp_width(altitude, distance):  # Compensating for angle caused by distance from target
    adjusted_width = (altitude * 40) / (distance + 20)
    return adjusted_width * 5580.2 * altitude ** -1.117


def get_tarp_length(altitude):
    return 40 * 5580.2 * altitude ** -1.117


def get_tarp_area(altitude, distance):
    return (get_tarp_width(altitude, distance) * 2) + (get_tarp_length(altitude) * 2)


def get_total_tarp_area(altitude, distance):
    return get_tarp_area(altitude, distance) * 3
