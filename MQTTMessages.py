from myutils import Byte
from protocol_constants import ControlType
from variable_headers import VariableHeader


class FixedHeader(object):
    length = 2  # Fixed length of 2 bytes!
    control_packet_type = None
    flags = 0
    formatted_flags = None

    # The Remaining Length is the number of bytes remaining within the current packet, including data in the variable
    # header and the payload. The Remaining Length does not include the bytes used to encode the Remaining Length.
    remaining_length = 0

    @staticmethod
    def parse(data):
        res = FixedHeader()
        # Parse the variable header
        if len(data) < 2:
            raise Exception("Invalid data. Fixed header should be at least 2 bytes")
        first_byte = Byte(data[0])
        res.control_packet_type = ControlType(first_byte._high_nibble())
        res.flags = first_byte._low_nibble()
        res.formatted_flags = first_byte.low_nibble
        res.remaining_length = FixedHeader.parse_remaining_length(data[1:])

        return res

    @staticmethod
    def parse_remaining_length(data):
        counter = 0
        multiplier = 1
        value = 0
        while True:
            encodedByte = data[counter]
            value += (encodedByte & 127) * multiplier
            multiplier *= 128

            if multiplier > (128 * 128 * 128):
                raise Exception("Malformed Remaining Length")

            if not ((encodedByte & 128) != 0):
                break
            counter += 1

        return value

    def __str__(self):
        res = "Type: %s\n" \
              "Flags: %s\n" \
              "Remaining length: %d" % (self.control_packet_type, self.formatted_flags, self.remaining_length)
        return res


class MQTTPacket(object):
    header = None  # type:FixedHeader
    vheader = None
    payload = None

    @staticmethod
    def parse(data):
        res = MQTTPacket()
        cursor = 0

        # Parse the fixed header. The fixed header is 2 bytes long
        res.header = FixedHeader.parse(data[cursor:])
        cursor += 2

        # Parse the variable header.
        res.vheader = VariableHeader.parse(res.header.control_packet_type, data[cursor:])
        cursor += res.vheader.length

        # Set the payload
        res.payload = data[cursor:]

        return res

    def __str__(self):
        return "================================\n" \
               "-----------FIXED HEADER---------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "--------VARIABLE HEADER---------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "------------PAYLOAD-------------\n" \
               "[Length]: %d bytes\n" \
               "%s\n" \
               "================================\n" % (self.header.length, str(self.header), self.vheader.length,  str(self.vheader), len(self.payload), str(self.payload))


if __name__ == '__main__':
    # Interpret the message as binary data
    data = b"\x10\x7f\x00\x04MQTT\x04\xc2\x00\x1e\x008fmware:18050329735693251a0234298f1178ce_K6sC3PCs9b360000\x00\x1134:29:8f:11:78:ce\x00&46884_858d2e3a3a1aab502657d3a0473d95f3"
    packet = MQTTPacket.parse(data)
    print(packet)