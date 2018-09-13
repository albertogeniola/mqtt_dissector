import struct


class Byte(object):
    """Do cool things with a 8 bit number"""

    def __init__(self, number):
        if not self.__isbyte(number):
            raise Exception('"%s" is not a 8 bit integer' % number)
        self.number = number

    def __isint(self, number):
        """Check if a input is of type int"""
        if type(number) == int:
            return True

    def __isbyte(self, number):
        """Check if a input is a byte, 0 - 255"""
        if self.__isint(number):
            if len(bin(number)[2:]) <= 8:
                return True

    def __format(self, num, size=8):
        """Format a number as binary with leading zeros"""
        return str(bin(num)[2:]).zfill(size)

    @property
    def binary(self):
        """Return Byte in binary"""
        return self.__format(self.number)

    def _high_nibble(self):
        """Use Bitwise shift to get high nibble from byte"""
        return self.number >> 4

    @property
    def high_nibble(self):
        """Return High Nibble in binary"""
        return self.__format(self._high_nibble(), 4)

    def _low_nibble(self):
        """Use Bitwise AND to get low nibble"""
        return self.number & 0x0F  # 0x0F == 15

    @property
    def low_nibble(self):
        """Return Low Nibble in binary"""
        return self.__format(self._low_nibble(), 4)


def parse_utf8_prefixed_string(data):
    cursor = 0
    length = struct.unpack(">H", data[cursor:cursor + 2])[0]
    cursor += 2

    string = data[cursor:cursor + length]
    cursor += length

    return str(string, "utf8"), cursor
