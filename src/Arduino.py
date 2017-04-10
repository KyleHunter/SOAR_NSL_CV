import smbus
import time


class Arduino:
    bus = smbus.SMBus(1)
    address = 0x04
    ALTREQ, ERRORCODEREQ, DISTREQ, INITREQ, INITDOFREQ, INITGPSREQ, GPSFIXREQ, SHUTDOWNREQ, LATREQ, LONREQ, \
        ISDEPLOYEDREQ, ORIENTATIONSREQONE, ORIENTATIONSREQTWO, ORIENTATIONSREQTHREE = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13

    def __init__(self, ei):
        self.ei = ei

    @staticmethod
    def convert_to_chars(item):
        return [ord(x) for x in str(item)]

    @staticmethod
    def convert_from_chars(item_array):
        return "".join([chr(i) for i in item_array])

    def read_bytes(self, cmd):
        char_array = self.bus.read_i2c_block_data(self.address, cmd)
        new_array = []
        for i in char_array:
            if i is 0:
                break
            new_array.append(i)

        return self.convert_from_chars(new_array)

    def _write_byte(self, value):
        self.bus.write_byte(self.address, value)
        time.sleep(0.05)

    def _read_byte(self):
        try:
            return self.bus.read_byte(self.address)
        except:
            print("Caught")

    def get_lattitude(self):
        return self.read_bytes(self.LATREQ)

    def get_longitude(self):
        return self.read_bytes(self.LONREQ)

    def get_altitude(self):
        return self.read_bytes(self.ALTREQ)

    def get_distance(self):
        return self.read_bytes(self.DISTREQ)

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
        or_zero = self.read_bytes(self.ORIENTATIONSREQONE)
        time.sleep(0.1)
        or_one = self.read_bytes(self.ORIENTATIONSREQTWO)
        time.sleep(0.1)
        or_two = self.read_bytes(self.ORIENTATIONSREQTHREE)
        return or_zero, or_one, or_two

    def init(self):
        self._write_byte(self.INITREQ)
        byte_one = self._read_byte()
        if byte_one:
            return False
        else:
            return True
