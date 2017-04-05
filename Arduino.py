import smbus
import time


class Arduino:
    bus = smbus.SMBus(1)
    address = 0x04
    ALTREQONE, ALTREQTWO, ERRORCODEREQ, DISTREQONE, DISTREQTWO, INITREQ, \
    INITDOFREQ, INITGPSREQ, GPSFIXREQ, SHUTDOWN, LATREQONE, LATREQTWO, LATREQTHREE, \
    LATREQFOUR, LONREQONE, LONREQTWO, LONREQTHREE, LONREQFOUR, \
        = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17

    def __init__(self, ei):
        self.ei = ei

    def _write_number(self, value):
        self.bus.write_byte(self.address, value)
        time.sleep(0.2)

    def _read_number(self):
        return self.bus.read_byte(self.address)

    def get_lattitude(self):
        self._write_number(self.LATREQONE)
        byte_one = self._read_number()

        self._write_number(self.LATREQTWO)
        byte_two = self._read_number()

        self._write_number(self.LATREQTHREE)
        byte_three = self._read_number()

        self._write_number(self.LATREQFOUR)
        byte_four = self._read_number()
        return float(str(byte_one) + "." + str(byte_two) + str(byte_three) + str(byte_four))

    def get_longitude(self):
        self._write_number(self.LONREQONE)
        byte_one = self._read_number()

        self._write_number(self.LONREQTWO)
        byte_two = self._read_number()

        self._write_number(self.LONREQTHREE)
        byte_three = self._read_number()

        self._write_number(self.LONREQFOUR)
        byte_four = self._read_number()
        return float(str(byte_one) + "." + str(byte_two) + str(byte_three) + str(byte_four))

    def get_altitude(self):
        self._write_number(self.ALTREQONE)
        byte_one = self._read_number()

        self._write_number(self.ALTREQTWO)
        byte_two = self._read_number()
        return int(str(byte_one) + str(byte_two))

    def get_distance(self):
        self._write_number(self.DISTREQONE)
        byte_one = self._read_number()

        self._write_number(self.DISTREQTWO)
        byte_two = self._read_number()
        return int(str(byte_one) + str(byte_two))

    def get_dof_error(self):
        self._write_number(self.INITDOFREQ)
        return self._read_number()

    def get_gps_error(self):
        self._write_number(self.INITGPSREQ)
        return self._read_number()

    def gps_has_fix(self):
        self._write_number(self.GPSFIXREQ)
        return self._read_number()

    def init(self):
        self._write_number(self.INITREQ)
        byte_one = self._read_number()
        if byte_one != self.INITREQ:
            return False
        else:
            return True
