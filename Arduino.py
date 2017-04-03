import smbus
import time


class Arduino:
    bus = smbus.SMBus(1)
    address = 0x04
    ALTREQONE, ALTREQTWO, ERRORCODEREQ, DISTREQONE, DISTREQTWO, INITREQ, \
    INITDOFREQ, INITGPSREQ, GPSFIXREQ, = 0, 1, 2, 3, 4, 5, 6, 7, 8

    def __init__(self, ei):
        self.ei = ei

    def _write_number(self, value):
        self.bus.write_byte(self.address, value)

    def _read_number(self):
        number = self.bus.read_byte(self.address)
        return number

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
