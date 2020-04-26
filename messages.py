from fixed_headers import FixedHeader
from payloads import Payload
from variable_headers import VariableHeader


class MQTTPacket(object):

    def __init__(self, header=None, vheader=None, payload=None):
        self.header = header    # type:FixedHeader
        self.vheader = vheader  # type: VariableHeader
        self.payload = payload  # type: Payload

    @staticmethod
    def parse(data):
        res = MQTTPacket()
        cursor = 0

        # Parse the fixed header. The fixed header is 2 bytes long
        res.header = FixedHeader.parse(data[cursor:])
        cursor += res.header.length

        # Parse the variable header.
        res.vheader = VariableHeader.parse(res.header, data[cursor:])
        cursor += res.vheader.length

        # Parse the payload
        res.payload = Payload.parse(res.header, res.vheader, data[cursor:])

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
               "================================\n" % (self.header.length, str(self.header), self.vheader.length,  str(self.vheader), self.payload.length, str(self.payload))

    def inline_str(self):
        return f"{self.header.control_packet_type.name}: {self.payload}"
