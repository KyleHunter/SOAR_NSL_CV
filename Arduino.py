import smbus
import time


class Arduino:
    bus = smbus.SMBus(1)
    address = 0x04
    ALTREQONE, ALTREQTWO, ERRORCODEREQ, DISTREQONE, DISTREQTWO = 0, 1, 2, 3, 4

    def __init__(self, ei):
        self.ei = ei

    def write_number(self, value):
        self.bus.write_byte(self.address, value)

    def read_number(self):
        number = self.bus.read_byte(self.address)
        return number

    def get_altitude(self):
        self.write_number(self.ALTREQONE)
        byte_one = self.read_number()

        self.write_number(self.ALTREQTWO)
        byte_two = self.read_number()
        return int(str(byte_one) + str(byte_two))

    def get_distance(self):
        self.write_number(self.DISTREQONE)
        byte_one = self.read_number()

        self.write_number(self.DISTREQTWO)
        byte_two = self.read_number()
        return int(str(byte_one) + str(byte_two))