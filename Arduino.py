import smbus
import time


class Arduino:
    bus = smbus.SMBus(1)
    address = 0x04
    ALTREQ, ERRORCODEREQ, DISTREQ, INITREQ, INITDOFREQ, INITGPSREQ, GPSFIXREQ, SHUTDOWNREQ, LATREQ, LONREQ, \
        ISDEPLOYEDREQ, ORIENTATIONSREQ = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11

    def __init__(self, ei):
        self.ei = ei

    @staticmethod
    def convert_to_chars(item):
        return [ord(x) for x in str(item)]

    @staticmethod
    def convert_from_chars(item_array):
        return "".join([chr(i) for i in item_array])

    def read_bytes(self):
        char_array, curr_char = [], -1

        while curr_char is not 0:
            curr_char = self._read_byte()
            if curr_char is not 0:
                char_array.append(curr_char)

        return self.convert_from_chars(char_array)

    def _write_byte(self, value):
        self.bus.write_byte(self.address, value)
        time.sleep(0.05)

    def _read_byte(self):
        return self.bus.read_byte(self.address)

    def get_lattitude(self):
        self._write_byte(self.LATREQ)
        return self.read_bytes()

    def get_longitude(self):
        self._write_byte(self.LONREQ)
        return self.read_bytes()

    def get_altitude(self):
        self._write_byte(self.ALTREQ)
        return self.read_bytes()

    def get_distance(self):
        self._write_byte(self.DISTREQ)
        return self.read_bytes()

    def get_dof_error(self):
        self._write_byte(self.INITDOFREQ)
        return self._read_byte()

    def get_gps_error(self):
        self._write_byte(self.INITGPSREQ)
        return self._read_byte()

    def gps_has_fix(self):
        self._write_byte(self.GPSFIXREQ)
        return self._read_byte()

    def lander_is_deployed(self):
        self._write_byte(self.ISDEPLOYEDREQ)
        return self._read_byte()

    def shutdown(self):
        self._write_byte(self.SHUTDOWNREQ)

    def get_orientations(self):
        self._write_byte(self.ORIENTATIONSREQ)
        or_zero = self.read_bytes()
        or_one = self.read_bytes()
        or_two = self.read_bytes()
        return or_zero, or_one, or_two

    def init(self):
        self._write_byte(self.INITREQ)
        byte_one = self._read_byte()
        if byte_one:
            return False
        else:
            return True
